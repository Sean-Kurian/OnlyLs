import flet
from APIGetter import APIGetter
import webbrowser
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Window(flet.UserControl): 
    def __init__(self): 
        super().__init__()

    def build(self): 
        self._players = []
        self._api_getter = APIGetter()
        
        player_names = self._api_getter.get_player_data()
        for i in range(0, 5): 
            if i < len(player_names): 

                self._players.append(flet.TextButton(text=player_names[i], data=player_names[i], on_click=self.get_op_gg_single))
            else: 
                self._players.append(flet.TextButton(text='N/A', data='', on_click=self.get_op_gg_single))

        print(resource_path("bg.png"))
        return flet.Column(
            controls=[
                flet.Container(
                    width=400,
                    height=800,
                    image_src = resource_path("images\\bg.png"),
                    #gradient is backup for when image isn't working
                    gradient=flet.LinearGradient(
                        colors=[
                            '#8c00fc',
                            '#9c14fc',
                            '#af2efa',
                            '#c74ef4',
                            '#de6df1',
                            '#ed81ee',
                        ], 
                        stops=[0.0,0.2,0.4,0.6,0.8,1.0]
                    ),
                    image_fit = flet.ImageFit.COVER,
                    margin=-10,
                    padding=25,
                    content=flet.Column(
                        controls=[
                            flet.Container(
                                width=400,
                                height=200,

                                content=flet.Row(
                                    alignment='center',
                                    spacing=20,

                                    controls=[
                                        flet.ElevatedButton(

                                            text='Refresh',
                                            bgcolor=flet.colors.BLUE_GREY_100,
                                            color=flet.colors.BLACK,
                                            on_click=self.set_names,
                                            data='Refresh Names',
                                        ),
                                        flet.ElevatedButton(
                                            text='OP.GG',
                                            bgcolor=flet.colors.BLUE_GREY_100,
                                            color=flet.colors.BLACK,
                                            on_click=self.get_op_gg_multi,
                                            data='OP.GG',
                                        )
                                    ]
                                )
                            ),
                            flet.Container(
                                width=400,
                                height=500,
                                content=flet.Column(
                                    horizontal_alignment='center',
                                    spacing=50,

                                    controls=[
                                        self._players[0],
                                        self._players[1],
                                        self._players[2],
                                        self._players[3],
                                        self._players[4],
                                    ]
                                )
                            )
                        ]
                    )
                )
            ]
        )

    def set_names(self, e): 
        player_names = self._api_getter.get_player_data()
        for i in range(0, 5): 
            if i < len(player_names): 
                self._players[i].text = player_names[i]
                self._players[i].data = player_names[i]
            else: 
                self._players[i].text = 'N/A'
                self._players[i].data = ''
        self.update()

    def get_op_gg_single(self, e): 
        print(e.control.data)
        if e.control.data:
            url = self._api_getter.get_single_lookup_opgg(e.control.data)
            webbrowser.open(url=url, new=0, autoraise=True)
        self.update()        

    def get_op_gg_multi(self, e): 
        player_data = self._api_getter.get_player_data()
        if player_data: 
            self.set_names(player_data)
            print('hiewr', player_data)
            url = self._api_getter.get_multi_lookup_opgg(player_data)
            webbrowser.open(url=url, new=0, autoraise=True)
        self.update()        

    