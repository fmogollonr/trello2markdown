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
                        #f.write(action['date'])
                        #f.write(action['memberCreator']['fullName'])
                        #print(action['data']['text']+"\n")
                        #print(action['date']+"\n")
                        #print(action['memberCreator']['fullName']+"\n")

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
                    #print(url)
                    url=re.sub("trello.com","api.trello.com",adjunto['url'])
                    url2=url+"?key="+key+"&token="+token
                    #print(url2)
                    descarga = requests.get(re.sub("trello.com","api.trello.com",adjunto['url']))
                    adjunto_name= adjunto['url'].split("/")
                    #print(adjunto['url'])
                    #print(adjunto['url']+"?key="+key+"&token="+token)
                    adjunto_nombre=re.sub('[^a-zA-Z0-9\.]','_', adjunto_name[len(adjunto_name)-1])
                    output_file_adjunto=os.path.join(adjuntos_folder, adjunto_nombre)
                    #open(output_file_adjunto, "wb").write(descarga.content)

                    #urllib.request.urlretrieve(adjunto['url'], output_file_adjunto)
                    #try:
                    #    open(output_file_adjunto, "wb").write(descarga.content)
                    #    f.write("\n## Adjuntos \n")
                    #    f.write("* !["+adjunto_name+"](adjuntos/"+adjunto_name+")\n")
                    #
                    #except OSError as error:
                    #    print(error)
                    print('Saving attachment', adjunto_nombre)
                    try:
                        print(url2)
                        adjunto="https://trello.com/1/cards/5ed6014fc9c47f17c4f131b1/attachments/5ee1e4131ce0582890e15ab5/download/TELIT_ongoing.png"
                        content = requests.get(url2,stream=True,timeout=60)
                        print(content.request.headers)
                    except Exception:
                        print("Error descargando")
                        continue
                    
                    with open(adjunto_nombre, 'wb') as f:
                        for chunk in content.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)                    
            
            f.close()
        #print(sublists_list)
        #card_url="https://api.trello.com/1/lists/"+sublists_list['id']+"/card?key="+key+"&token="+token
        #print(sublists_list['id'])
        #print(card_url)
        #c=requests.get(card_url)
        #cards_list=c.json()
        #print("cards_list")
        #print(cards_list)
        #for answer_card in cards_list:
            #print(answer_card)
            #print(answer_card['id'])
            #print(answer_card['name'])

