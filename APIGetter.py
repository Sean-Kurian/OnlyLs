import base64
import json
import psutil
import requests
from urllib.parse import urlencode


class APIGetter: 
    def __init__(self): 
        #declare and initialize the necessary fields
        self._league_client = 'LeagueClientUx.exe'
        self._shell=None
        self._lockfile=None
        self._lcu_auth_token=None

        for proc in psutil.process_iter(): 
            if proc.name() == self._league_client: 
                str = proc.exe()
                repl = {'\\':'/', 'LeagueClientUx.exe':''}
                for i, j in repl.items():
                    str = str.replace(i, j)
                self._lockfile = str + 'lockfile' 
                self._shell = proc.cmdline()
                #Lockfile format-> Process Name : Process ID : Port : Password : Protocol
                with open(self._lockfile, 'r') as f:
                    file_data = f.read().split(':')
                    self._lcu_auth_token = base64.b64encode(('riot:' + file_data[3]).encode('ascii')).decode('ascii')
        
        #check if LoL is running: if not, quit the program
        if self._shell==None:
            exit("League of Legends should be running in order to use this tool.\nQUITTING!\n")

        for line in self._shell:
            if '--region=' in line:
                print(line.split('region', 1)[1].lower())
                self._region = line.split('region=', 1)[1].lower()
            elif '--remoting-auth-token=' in line:
                self._auth_token = line.split('remoting-auth-token=', 1)[1]
            elif '--app-port=' in line:
                self._app_port = line.split('app-port=', 1)[1]
            elif '--riotclient-auth-token=' in line:
                raw_token = line.split('riotclient-auth-token=', 1)[1]
                self._riot_client_auth_token = base64.b64encode(('riot:' + raw_token).encode('ascii')).decode(
            'ascii')
            elif '--riotclient-app-port=' in line:
                raw_port = line.split('riotclient-app-port=', 1)[1]      
                self._riot_client_port = 'https://127.0.0.1:' + raw_port

    def get_player_data(self): 
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'LeagueOfLegendsClient',
            'Authorization': 'Basic ' + self._riot_client_auth_token,
        }

        req = requests.get(self._riot_client_port + '/chat/v5/participants/champ-select', verify=False, headers=headers)
        data = json.loads(req.text)
        print([player['name'] for player in data['participants']])

        return [player['name'] for player in data['participants']]

    def get_multi_lookup_opgg(self, names): 
        base_url = f'https://www.op.gg/multisearch/{self._region}?'
        params = {'summoners': ','.join(names)}
        return base_url + urlencode(params)
    
    def get_single_lookup_opgg(self, name): 
        base_url = 'https://www.op.gg/summoners/'
        param = self._region + '/' + name
        return base_url + param

test = APIGetter()
name = test.get_player_data()
test.get_single_lookup_opgg('Intrinsically')
