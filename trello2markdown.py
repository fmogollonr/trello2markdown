import requests
import os
import re
import urllib.request
import json
import sys


parent_dir=sys.argv[1]
key=sys.argv[2]
token=sys.argv[3]
path = os.path.join(parent_dir, "trello_backup")

def get_board (answers,archived=False):
    for answer in answers:
        print(answer['name'])
        output_folder = os.path.join(path, answer["name"])
        if archived == True:
            output_folder = os.path.join(path, answer["name"]+"_archived")

        try:
            os.mkdir(output_folder)
        except OSError as error:
            print("Cannot mkdir "+output_folder)
            print(error)
        list_url="https://api.trello.com/1/boards/"+answer['id']+"/lists"
        if archived == True:
            list_url="https://api.trello.com/1/boards/"+answer['id']+"/lists?filter=closed"

        l=requests.get(list_url,headers=myheaders)
        answers_list=l.json()
        for answer_list in answers_list:
            sublist_url="https://api.trello.com/1/lists/"+answer_list['id']+"/cards?attachments=true"
            s=requests.get(sublist_url,headers=myheaders)
            sublists_list=s.json()
            output_file=os.path.join(output_folder, answer_list['name']+".md")
            if archived == True:
                output_file=os.path.join(output_folder, answer_list['name']+"_archived.md")
            try:
                os.remove(output_file)
            except:
                print("Cannot remove: doesnt exists "+output_file) 

            for card in sublists_list:
                output_file=os.path.join(output_folder, answer_list['name']+".md")
                if archived == True:
                    output_file=os.path.join(output_folder, answer_list['name']+"_archived.md")
                f = open(output_file, "a")
                f.write("# "+card['name']+"\n")
                f.write(card['desc'])
                if len(card['labels']) > 0:
                    f.write('\n## Etiquetas\n')
                for etiqueta in card['labels']:
                    f.write("* "+etiqueta['name']+"\n")
                member_request=requests.get("https://api.trello.com/1/cards/"+card['id']+"/members",headers=myheaders)
                member_content=json.loads(member_request.content.decode('utf-8'))
                if len(member_content) > 0:
                    f.write('\n## Members\n')
                for member in member_content:
                    #print(member['username'])
                    f.write("* "+member['username']+"\n")
                actions_url="https://api.trello.com/1/cards/"+card['id']+"/actions"
                actions_request=requests.get(actions_url,headers=myheaders)
                actions=parsed = json.loads(actions_request.content)
                for action in actions:
                    if action['type'] == "commentCard":
                        if action['data']['card']['id'] == card['id']:
                            try action['memberCreator']:
                                f.write('\n## Comentario el '+action['date']+' por '+action['memberCreator']['fullName']+'\n')
                            except:
                                f.write('\n## Comentario el '+action['date']+' por autor desconocido\n')
                            f.write(action['data']['text']+'\n')

                if len(card['attachments']) > 0:
                    adjuntos_folder = os.path.join(output_folder,"adjuntos")
                    try:
                        os.mkdir(adjuntos_folder)
                    except OSError as error:
                        print("Cannot mkdir "+output_file)
                        print(error)
                    attach_request="https://api.trello.com/1/cards/"+card['id']+"/attachments/?fields=url"
                    adjunto_respuesta=requests.get(attach_request,headers=myheaders)
                    parsed = json.loads(adjunto_respuesta.content)
                    for adjunto in parsed:
                        url=re.sub("trello.com","api.trello.com",adjunto['url'])
                        descarga = requests.get(url,headers=myheaders)
                        adjunto_name= adjunto['url'].split("/")
                        adjunto_nombre=re.sub('[^a-zA-Z0-9\.]','_', adjunto_name[len(adjunto_name)-1])
                        output_file_adjunto=os.path.join(adjuntos_folder, adjunto_name[len(adjunto_name)-1])
                        try:
                            open(output_file_adjunto, "wb").write(descarga.content)
                            f.write("\n## Adjuntos \n")
                            f.write("* !["+adjunto_name[len(adjunto_name)-1]+"](adjuntos/"+adjunto_name[len(adjunto_name)-1]+")\n")

                        except OSError as error:
                            print("cannot write "+output_file_adjunto)
                            print(error)
                        print('Saving attachment', adjunto_name[len(adjunto_name)-1])

                f.close()



try:
    os.mkdir(path)
except OSError as error:
    print(error)   

myheaders = { 'Authorization': 'OAuth oauth_consumer_key="'+key+'", oauth_token="'+token+'"' }


# get boards
boards_url="https://api.trello.com/1/members/me/boards/"
r=requests.get(boards_url, headers=myheaders)
answers=r.json()


get_board(answers)
get_board(answers,True)


try:
    os.mkdir(path)
except OSError as error:
    print(error)   

# get boards
boards_url="https://api.trello.com/1/members/me/boards/?key="+key+"&token="+token
r=requests.get(boards_url)

answers=r.json()
#print(r.json())

for answer in answers:
    #print(answer['id'])
    #print(answer['name'])
    output_folder = os.path.join(path, answer["name"])
    try:
        if os.path.exists(output_folder) is False:
            os.mkdir(output_folder)
    except OSError as error:
        print(error)
    list_url="https://api.trello.com/1/boards/"+answer['id']+"/lists?key="+key+"&token="+token
    l=requests.get(list_url)
    answers_list=l.json()
    for answer_list in answers_list:
        #print(answer_list['id'])
        #print(answer_list['name'])


        sublist_url="https://api.trello.com/1/lists/"+answer_list['id']+"/cards?key="+key+"&token="+token+"&attachments=true"
        #print(card_url)
        s=requests.get(sublist_url)
        #print("sublist")
        sublists_list=s.json()
        output_file=os.path.join(output_folder, answer_list['name']+".md")
        try:
            os.remove(output_file)
        except:
            print("doesnt exists") 

        for card in sublists_list:
            print(card['id'])
            output_file=os.path.join(output_folder, answer_list['name']+".md")
            f = open(output_file, "a")
            f.write("# "+card['name']+"\n")
            f.close()
            f = open(output_file, "a")
            f.write(card['desc'])
            if len(card['labels']) > 0:
                f.write('\n## Etiquetas\n')
            for etiqueta in card['labels']:
                #print(etiqueta['name'])
                f.write("* "+etiqueta['name']+"\n")
            #print(card['attachments'])
            #print("get actions")
            actions_url="https://api.trello.com/1/cards/"+card['id']+"/actions?key="+key+"&token="+token
                    #print(url)
            actions_request=requests.get(actions_url)
            actions=parsed = json.loads(actions_request.content)
            for action in actions:
                if action['type'] == "commentCard":
                    if action['data']['card']['id'] == card['id']:
                        f.write('\n## Comentario el '+action['date']+' por '+action['memberCreator']['fullName']+'\n')
                        f.write(action['data']['text']+'\n')

            if len(card['attachments']) > 0:
                #print("adjuntos")
                adjuntos_folder = os.path.join(path,"adjuntos")
                try:
                    os.mkdir(adjuntos_folder)
                except OSError as error:
                    print(error)
                attach_request="https://api.trello.com/1/cards/"+card['id']+"/attachments/?fields=url&key="+key+"&token="+token
                adjunto_respuesta=requests.get(attach_request)
                parsed = json.loads(adjunto_respuesta.content)
                #print(parsed)
                for adjunto in parsed:
                    print(adjunto['url'])
                    url="https://api.trello.com/1/cards/"+card['id']+"/attachments/"+adjunto['id']+"?key="+key+"&token="+token
                    url=re.sub("trello.com","api.trello.com",adjunto['url'])
                    url2=url+"?key="+key+"&token="+token
                    descarga = requests.get(re.sub("trello.com","api.trello.com",adjunto['url']))
                    adjunto_name= adjunto['url'].split("/")
                    adjunto_nombre=re.sub('[^a-zA-Z0-9\.]','_', adjunto_name[len(adjunto_name)-1])
                    output_file_adjunto=os.path.join(adjuntos_folder, adjunto_nombre)
                    print('Saving attachment', adjunto_nombre)
                    try:
                        content = requests.get(url2,stream=True,timeout=60)
                        #print(content.request.headers)
                    except Exception:
                        print("Error descargando")
                        continue
                    try:
                        with open(adjunto_nombre, 'wb') as f:
                            for chunk in content.iter_content(chunk_size=1024):
                                if chunk:
                                    f.write(chunk)
                    except IOError:
                        print("Error")
            
            f.close()
