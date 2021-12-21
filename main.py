from kivy.uix.popup import Popup
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen,ScreenManager
from kivymd.uix.list import TwoLineAvatarIconListItem, ImageLeftWidget,ThreeLineAvatarIconListItem
from kivymd.uix.picker import MDDatePicker
from plyer import filechooser
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
import time
import datetime
from datetime import datetime,date

from kivy.config import Config
import sqlite3


Config.set('graphics', 'resizable', True)
TRIPS_SELECTED = []
lista = []
adding = []
ading = []
id = []
li = []
valus = []
oda = []
daterang = []
dialog = None

screen_helper = """
#: import utils kivy.utils
MDNavigationLayout:
    cols:1
    ScreenManager:
        id: screenmanager
        HomeScreen:
            id:home
            name:'home'
        WelcomeScreen:
            id:welcomescreen
            name:'welcomescreen'
        AddExpense:
            id:add_expense
            name: 'add_expense'
        Content:
            id:content
            name:'content'
        Customers:
            id:customers
            name:'customers'
        Menu:
            id:menu
            name:'menu'
        UpdateMenu:
            id:updatemenu
            name:'updatemenu'
        UpdateCustomer:
            id:updatecustomer
            name:'updatecustomer'
        UpdateExpenses:
            id:updateexpenses
            name:'updateexpenses'
        UpdateOrder:
            id:updateorder
            name:'updateorder'
        Expenses:
            id:expenses
            name:'expenses'
        Imagepreview:
            id:imagepreview
            name:'imagepreview'
        Avata:
            id:avata
            name:'avata'
        Order:
            id:order
            name:'order'
        SplashScreen:
            id:splashscreen
            name:'splashscreen'
        Expensetable:
            id:expensetable
            name:'expensetable'
        CustomerTable:
            id:customertable
            name:'customertable'
<WelcomeScreen>
    FloatLayout:
        canvas.before:
            Color:
                rgb: utils.get_color_from_hex('#CDD4E4')
            Rectangle:
                size: self.size
                pos: self.pos
        
        FloatLayout:
            Image:
                id:img
                source: 'kenyaneats.jpg'
                allow_stretch: True
                size_hint:1,1
            
            MDTextField:
                id:menu_name
                hint_text: "Enter Password"
                text_color: app.theme_cls.primary_color
                helper_text: "this field must be filled"
                helper_text_mode: "on_focus"
                icon_right: "robot-excited"
                icon_right_color: app.theme_cls.primary_color
                pos_hint:{'center_x': 0.5, 'center_y': 0.3}
                size_hint_x:None
                width:300
                password: True
            MDFloatingActionButton:
                icon: "arrow-right"
                pos_hint:{'center_x': .8, 'center_y': .3}
                on_release:
                    app.post_login()
                    
            
<SplashScreen>:
    FloatLayout:
        canvas.before:
            Color:
                rgb: utils.get_color_from_hex('#CDD4E4')
            Rectangle:
                size: self.size
                pos: self.pos

        Label:
            text: str(app.total_earning) + '/' + str(app.budget) + " "+'KSH'
            pos_hint:{'top':.85}
            size_hint:1,.1
            font_size:30
            color:0,0,0,1
        MDRaisedButton:
            text:'Specific Date'
            pos_hint:{'top':.90,'left':1}
            size_hint:.4,.06
            on_release:
                app.specific_date_picker()
                app.clearoder()
        
        MDRaisedButton:
            text: "Date Range"
            pos_hint:{'top':.90,'right':1}
            size_hint:.4,.06
            on_release:
                app.show_date_picker()
                app.clearoder()
        

        ScrollView:
            pos_hint:{'center_x': .5}
            size_hint_y:.80
            MDGridLayout:
                cols:1
                size_hint_x:.5

                adaptive_height: True
                id: expense_list
        ScrollView:
            pos_hint:{'center_x': .7}
            size_hint_y:.80
            MDGridLayout:
                cols:1
                size_hint_x:.7

                adaptive_height: True
                id: list
        ScrollView:
            pos_hint:{'center_x': 1}
            size_hint_y:.80
            MDGridLayout:
                cols:1
                size_hint_x: .7

                adaptive_height: True
                id: expense_lis
        MDFloatingActionButtonSpeedDial:
            data:app.data
            root_button_anim: True
            bg_hint_color:1,0,0,1
            callback:app.callback
        MDToolbar:
            id: toolbar
            pos_hint: {"top": 1}
            background_color: app.theme_cls.primary_dark
            elevation: 10
            title: "KENYAN EATS" + "   "+ str(app.today)+"   "+str(app.time)
            left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
        Widget:
        MDNavigationDrawer:
            id:nav_drawer
            opening_transition:'out_bounce'
            opening_time:1
            closing_transition:'in_out_elastic'
            closing_time:1
            BoxLayout:
                orientation:'vertical'
                spacing:'12dp'
                padding:'12dp'

                MDRectangleFlatIconButton:
                    pos_hint:{'top':.5}
                    icon:"android"
                    text:'Edit Menu'
                    size_hint_y: None
                    on_release:
                        app.tabol()
                        app.onstart()
                        app.change_screen('avata', "nothing")
                        nav_drawer.set_state("close")
                MDRectangleFlatIconButton:
                    pos_hint:{'top':.5}
                    icon:"android"
                    text:'Edit Expense'
                    size_hint_y: None
                    on_release:
                        app.EXPENSE_TBL()
                        app.onstart()
                        app.change_screen('expensetable', "nothing")
                        nav_drawer.set_state("close")
                MDRectangleFlatIconButton:
                    pos_hint:{'top':.5}
                    icon:"robot-happy"
                    text:'Edit Customers'
                    size_hint_y: None
                    on_release:
                        app.tabal()
                        app.onstart()
                        app.change_screen('customertable', "nothing")
                        nav_drawer.set_state("close")

                ScrollView:

<HomeScreen>:
    FloatLayout:
        canvas.before:
            Color:
                rgb: utils.get_color_from_hex('#CDD4E4')
            Rectangle:
                size: self.size
                pos: self.pos

        
        Label:
            text: str(app.total_earning) + '/' + str(app.budget) + " "+'KSH'
            pos_hint:{'top':.85}
            size_hint:1,.1
            font_size:30
            color:0,0,0,1
        MDRaisedButton:
            text:'Specific Date'
            pos_hint:{'top':.90,'left':1}
            size_hint:.4,.06
            on_release:
                app.specific_date_picker()
                app.clearoder()
        MDRaisedButton:
            text: "Date Range"
            pos_hint:{'top':.90,'right':.7}
            size_hint:.4,.06
            on_release:
                app.show_date_picker()
                app.clearoder()
        
        MDRaisedButton:
            text:'Stats'
            pos_hint:{'top':.90,'right':1}
            size_hint:.3,.06
            on_release:
                app.on_star()

        ScrollView:
            pos_hint:{'center_x': .5}
            size_hint_y:.75
            MDGridLayout:
                cols:1
                size_hint_x:.5

                adaptive_height: True
                id: expense_list
        ScrollView:
            pos_hint:{'center_x': .7}
            size_hint_y:.75
            MDGridLayout:
                cols:1
                size_hint_x:.7

                adaptive_height: True
                id: list
        ScrollView:
            pos_hint:{'center_x': 1}
            size_hint_y:.75
            MDGridLayout:
                cols:1
                size_hint_x: .7

                adaptive_height: True
                id: expense_lis
        MDFloatingActionButtonSpeedDial:
            data:app.data
            root_button_anim: True
            bg_hint_color:1,0,0,1
            callback:app.callback
        MDToolbar:
            id: toolbar
            pos_hint: {"top": 1}
            background_color: app.theme_cls.primary_dark
            elevation: 10
            title: "SLY CAFE" + "   "+ str(app.today)+"   "+str(app.time)
            left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
        Widget:
        MDNavigationDrawer:
            id:nav_drawer
            opening_transition:'out_bounce'
            opening_time:1
            closing_transition:'in_out_elastic'
            closing_time:1
            BoxLayout:
                orientation:'vertical'
                spacing:'12dp'
                padding:'12dp'

                MDRectangleFlatIconButton:
                    pos_hint:{'top':.5}
                    icon:"android"
                    text:'Edit Menu'
                    size_hint_y: None
                    on_release:
                        app.tabol()
                        app.onstart()
                        app.change_screen('avata', "nothing")
                        nav_drawer.set_state("close")
                MDRectangleFlatIconButton:
                    pos_hint:{'top':.5}
                    icon:"android"
                    text:'Edit Expense'
                    size_hint_y: None
                    on_release:
                        app.EXPENSE_TBL()
                        app.onstart()
                        app.change_screen('expensetable', "nothing")
                        nav_drawer.set_state("close")
                
                MDRectangleFlatIconButton:
                    pos_hint:{'top':.5}
                    icon:"robot-happy"
                    text:'Edit Customers'
                    size_hint_y: None
                    on_release:
                        app.tabal()
                        app.onstart()
                        app.change_screen('customertable', "nothing")
                        nav_drawer.set_state("close")

                ScrollView:
<AddExpense>:
    FloatLayout:
        Label:
            text:'Choose an image'
            pos_hint:{'top':1}
            size_hint:1,.1
            font_size:20
            color:0,0,0,1
        ScrollView:
            pos_hint:{'top':.9}
            size_hint:1,.15
            GridLayout:
                size_hint_x :None
                width: self.minimum_width
                col_default_width: '100dp'
                col_force_default: True
                id: expense_images
        ScrollView:
            pos_hint:{'top':.8}
            size_hint:1,.15
            GridLayout:
                size_hint_x :None
                width: self.minimum_width
                col_default_width: '100dp'
                col_force_default: True
                id: expense_images

        MDTextField:
            id: namefield
            pos_hint:{'top':.5,'left':1}
            size_hint:.4,.07
            hint_text:'Expense name'
            mode:'rectangle'
            on_focus: if self.focus: app.mon.open()
        MDTextField:
            id: moneyfield
            pos_hint:{'top':.5,'right':1}
            size_hint:.5,.07
            hint_text:'Money'
            mode:'rectangle'

        MDRaisedButton:
            text:'Back'
            pos_hint:{'top':.1,'left':.8}
            size_hint:.3,.04
            on_release:
                app.change_screen('home', "nothing")
<Content>
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "120dp"

    MDTextField:
        id: budget
        line_color_focus: 1, 0, 1, 1

<Customers>
    MDLabel:
        theme_text_color: "Custom"
        text_color: 0, 0, 1, 1
        font_size: 36
        text: "Add Customer"
        halign: "center"
        pos_hint:{'center_x': 0.5, 'center_y': 0.9}

    MDTextField:
        id:name
        hint_text: "Enter Name"
        helper_text: "this field must be filled"
        helper_text_mode: "on_focus"
        icon_right: "robot-excited"
        icon_right_color: app.theme_cls.primary_color
        pos_hint:{'center_x': 0.5, 'center_y': 0.7}
        size_hint_x:None
        width:300
    MDTextField:
        id:phone
        hint_text: "Enter Phone no."
        helper_text: "this field must be filled"
        helper_text_mode: "on_focus"
        icon_right: "phone"
        icon_right_color: app.theme_cls.primary_color
        pos_hint:{'center_x': 0.5, 'center_y': 0.6}
        size_hint_x:None
        width:300
    MDRoundFlatIconButton:
        icon: "briefcase-plus"
        text: "OK"
        pos_hint:{"center_x": .5, "center_y": .4}
        on_release:
            app.post_customers(name.text,phone.text)
    MDFloatingActionButton:
        icon: "arrow-left-thin-circle-outline"
        pos_hint:{'top':.1,'left':.8}
        on_release:
            app.change_screen('home',"nothing")

<Menu>
    MDLabel:
        theme_text_color: "Custom"
        text_color: 0, 0, 1, 1
        font_size: 36
        text: "Add Menu"
        halign: "center"
        pos_hint:{'center_x': 0.5, 'center_y': 0.9}
    MDTextField:
        id:menu_name
        hint_text: "Enter Menu Name"
        helper_text: "this field must be filled"
        helper_text_mode: "on_focus"
        icon_right: "robot-excited"
        icon_right_color: app.theme_cls.primary_color
        pos_hint:{'center_x': 0.5, 'center_y': 0.7}
        size_hint_x:None
        width:300
    MDTextField:
        id:menu_type
        hint_text: "Enter Menu Type."
        helper_text: "this field must be filled"
        helper_text_mode: "on_focus"
        icon_right: "phone"
        icon_right_color: app.theme_cls.primary_color
        pos_hint:{'center_x': 0.5, 'center_y': 0.6}
        size_hint_x:None
        width:300
    MDTextField:
        id:menu_price
        hint_text: "Enter Menu Price."
        helper_text: "this field must be filled"
        helper_text_mode: "on_focus"
        icon_right: "phone"
        icon_right_color: app.theme_cls.primary_color
        pos_hint:{'center_x': 0.5, 'center_y': 0.5}
        size_hint_x:None
        width:300
    
    MDRoundFlatIconButton:
        disabled:False
        icon: "folder-image"
        text: "Post"
        pos_hint:{"center_x": .5, "center_y": .4}
        on_release:
            app.post_menu()
    MDRoundFlatButton:
        text: "Back"
        icon: "arrow-left"
        pos_hint:{'top':.1,'left':.8}
        on_release:
            app.change_screen('splashscreen', "nothing")
            app.welcome()
<Imagepreview>  
    MDTextField:
        id:menu_name
        hint_text: "Enter Password"
        helper_text: "this field must be filled"
        helper_text_mode: "on_focus"
        icon_right: "robot-excited"
        icon_right_color: app.theme_cls.primary_color
        pos_hint:{'center_x': 0.5, 'center_y': 0.7}
        size_hint_x:None
        width:300
        password: True
    
<UpdateMenu>
    MDLabel:
        theme_text_color: "Custom"
        text_color: 0, 0, 1, 1
        font_size: 36
        text: "Edit Menu"
        halign: "center"
        pos_hint:{'center_x': 0.5, 'center_y': 0.9}
    MDTextField:
        id:menu_name
        hint_text: "Enter Menu Name"
        helper_text: "this field must be filled"
        helper_text_mode: "on_focus"
        icon_right: "robot-excited"
        icon_right_color: app.theme_cls.primary_color
        pos_hint:{'center_x': 0.5, 'center_y': 0.7}
        size_hint_x:None
        width:300
    MDTextField:
        id:menu_type
        hint_text: "Enter Menu Type."
        helper_text: "this field must be filled"
        helper_text_mode: "on_focus"
        icon_right: "phone"
        icon_right_color: app.theme_cls.primary_color
        pos_hint:{'center_x': 0.5, 'center_y': 0.6}
        size_hint_x:None
        width:300
    MDTextField:
        id:menu_price
        hint_text: "Enter Menu Price."
        helper_text: "this field must be filled"
        helper_text_mode: "on_focus"
        icon_right: "phone"
        icon_right_color: app.theme_cls.primary_color
        pos_hint:{'center_x': 0.5, 'center_y': 0.5}
        size_hint_x:None
        width:300

    
    MDRoundFlatButton:
        disabled:False
        icon: "folder-image"
        text: "Edit"
        pos_hint:{"center_x": .5, "center_y": .4}
        on_release:
            app.edit_menu()
            app.welcome()

    MDFloatingActionButton:
        icon: "arrow-left"
        pos_hint:{'center_x': .15, 'center_y': .1}
        on_release:
            app.change_screen('avata',"nothing")
            app.tabol()
<UpdateCustomer>
    MDLabel:
        theme_text_color: "Custom"
        text_color: 0, 0, 1, 1
        font_size: 36
        text: "Edit Customer"
        halign: "center"
        pos_hint:{'center_x': 0.5, 'center_y': 0.9}
    MDTextField:
        id:customer_name
        hint_text: "Enter Customer Name"
        helper_text: "this field must be filled"
        helper_text_mode: "on_focus"
        icon_right: "robot-excited"
        icon_right_color: app.theme_cls.primary_color
        pos_hint:{'center_x': 0.5, 'center_y': 0.7}
        size_hint_x:None
        width:300
    MDTextField:
        id:phone
        hint_text: "Enter Phone Number."
        helper_text: "this field must be filled"
        helper_text_mode: "on_focus"
        icon_right: "phone"
        icon_right_color: app.theme_cls.primary_color
        pos_hint:{'center_x': 0.5, 'center_y': 0.6}
        size_hint_x:None
        width:300

    MDRoundFlatButton:
        disabled:False
        icon: "folder-image"
        text: "Edit"
        pos_hint:{"center_x": .5, "center_y": .5}
        on_release:
            app.edit_customer()
            app.welcome()

    MDFloatingActionButton:
        icon: "arrow-left"
        pos_hint:{'center_x': .15, 'center_y': .1}
        on_release:
            app.change_screen('customertable',"nothing")
            app.tabal()
<UpdateOrder>
    MDLabel:
        theme_text_color: "Custom"
        text_color: 0, 0, 1, 1
        font_size: 36
        text: "Edit Order"
        halign: "center"
        pos_hint:{'center_x': 0.5, 'center_y': 0.9}
    MDTextField:
        id:customer_name
        hint_text: "Edit Customer"
        helper_text: "this field must be filled"
        helper_text_mode: "on_focus"
        icon_right: "robot-excited"
        icon_right_color: app.theme_cls.primary_color
        pos_hint:{'center_x': 0.5, 'center_y': 0.7}
        size_hint_x:None
        width:300
    MDTextField:
        id:order
        hint_text: "Edit Order"
        helper_text: "this field must be filled"
        helper_text_mode: "on_focus"
        icon_right: "phone"
        icon_right_color: app.theme_cls.primary_color
        pos_hint:{'center_x': 0.5, 'center_y': 0.6}
        size_hint_x:None
        width:300

    MDRoundFlatButton:
        disabled:False
        icon: "folder-image"
        text: "Edit"
        pos_hint:{"center_x": .5, "center_y": .5}
        on_release:
            app.edit_order()
            app.welcome()

    MDFloatingActionButton:
        icon: "arrow-left"
        pos_hint:{'center_x': .15, 'center_y': .1}
        on_release:
            app.change_screen('order',"nothing")
            app.ORDER_TBL()
<UpdateExpenses>
    MDLabel:
        theme_text_color: "Custom"
        text_color: 0, 0, 1, 1
        font_size: 36
        text: "Edit Expenses"
        halign: "center"
        pos_hint:{'center_x': 0.5, 'center_y': 0.9}
    MDTextField:
        id:expense_name
        hint_text: "Update Expense Name"
        helper_text: "this field must be filled"
        helper_text_mode: "on_focus"
        icon_right: "robot-excited"
        icon_right_color: app.theme_cls.primary_color
        pos_hint:{'center_x': 0.5, 'center_y': 0.7}
        size_hint_x:None
        width:300
    MDTextField:
        id:expense_quantity
        hint_text: "Update Expense Quantity."
        helper_text: "this field must be filled"
        helper_text_mode: "on_focus"
        icon_right: "phone"
        icon_right_color: app.theme_cls.primary_color
        pos_hint:{'center_x': 0.5, 'center_y': 0.6}
        size_hint_x:None
        width:300
    MDTextField:
        id:expense_price
        hint_text: "Update Expense Price."
        helper_text: "this field must be filled"
        helper_text_mode: "on_focus"
        icon_right: "phone"
        icon_right_color: app.theme_cls.primary_color
        pos_hint:{'center_x': 0.5, 'center_y': 0.5}
        size_hint_x:None
        width:300
    MDTextField:
        id:duration
        hint_text: "Update Item Duration."
        helper_text: "this field must be filled"
        helper_text_mode: "on_focus"
        icon_right: "phone"
        icon_right_color: app.theme_cls.primary_color
        pos_hint:{'center_x': 0.5, 'center_y': 0.4}
        size_hint_x:None
        width:300

    MDFloatingActionButton:
        icon: "arrow-left"
        pos_hint:{'center_x': .15, 'center_y': .2}
        on_release:
            app.change_screen('splashscreen',"nothing")
            app.welcome()

    MDFloatingActionButton:
        id:update
        icon: "update"
        pos_hint:{'center_x': .85, 'center_y': .2}
        on_release:
            app.edit_expense()
<Expenses>
    MDLabel:
        theme_text_color: "Custom"
        text_color: 0, 0, 1, 1
        font_size: 36
        text: "Add Expenses"
        halign: "center"
        pos_hint:{'center_x': 0.5, 'center_y': 0.9}
    MDTextField:
        id:expense_name
        hint_text: "Enter Expense Name"
        helper_text: "this field must be filled"
        helper_text_mode: "on_focus"
        icon_right: "robot-excited"
        icon_right_color: app.theme_cls.primary_color
        pos_hint:{'center_x': 0.5, 'center_y': 0.7}
        size_hint_x:None
        width:300
    MDTextField:
        id:expense_quantity
        hint_text: "Enter Expense Quantity."
        helper_text: "this field must be filled"
        helper_text_mode: "on_focus"
        icon_right: "phone"
        icon_right_color: app.theme_cls.primary_color
        pos_hint:{'center_x': 0.5, 'center_y': 0.6}
        size_hint_x:None
        width:300
    MDTextField:
        id:expense_price
        hint_text: "Enter Expense Price."
        helper_text: "this field must be filled"
        helper_text_mode: "on_focus"
        icon_right: "phone"
        icon_right_color: app.theme_cls.primary_color
        pos_hint:{'center_x': 0.5, 'center_y': 0.5}
        size_hint_x:None
        width:300
    MDTextField:
        id:duration
        hint_text: "Enter Duration of Item."
        helper_text: "this field must be filled"
        helper_text_mode: "on_focus"
        icon_right: "phone"
        icon_right_color: app.theme_cls.primary_color
        pos_hint:{'center_x': 0.5, 'center_y': 0.4}
        size_hint_x:None
        width:300

    MDRoundFlatIconButton:
        icon: "briefcase-plus"
        text: "OK"
        pos_hint:{"center_x": .5, "center_y": .3}
        on_release:
            app.post_expense()
    MDFloatingActionButton:
        icon: "arrow-left"
        pos_hint:{'center_x': .15, 'center_y': .15}
        on_release:
            app.change_screen('splashscreen',"nothing")
            app.welcome()

<Imageprevie>:
    FloatLayout:
        Image:
            id:img
            pos_hint:{'center_x': .5, 'center_y': .7}
            size_hint:.8,.8

        MDLabel:
            id: selected_path
            text:""
            halign:"center"
    MDFloatingActionButton:
        icon: "food-fork-drink"
        pos_hint:{'center_x': .5, 'center_y': .4}
        on_release:
            app.post_menu()
            app.change_screen('menu', "add")
            app.noti()
<Avata>:
    FloatLayout:
        id:ava
    MDFloatingActionButton:
        id:btn
        icon: "delete-circle-outline"
        pos_hint:{'center_x': .5, 'center_y': .2}
        on_release:
            app.on_check()

    MDFloatingActionButton:
        icon: "arrow-left"
        pos_hint:{'center_x': .15, 'center_y': .2}
        on_release:
            app.change_screen('splashscreen',"nothing")
            

    MDFloatingActionButton:
        id:update
        icon: "update"
        pos_hint:{'center_x': .85, 'center_y': .2}
        on_release:
            app.check(app.instance_table, app.current_row)
<Order>:
    FloatLayout:
        id:ava
    MDFloatingActionButton:
        id:btn
        icon: "delete-circle-outline"
        pos_hint:{'center_x': .5, 'center_y': .15}
        on_release:
            app.remove_order()

    MDFloatingActionButton:
        icon: "arrow-left"
        pos_hint:{'center_x': .15, 'center_y': .15}
        on_release:
            app.change_screen('splashscreen',"nothing")
            app.welcome()

    MDFloatingActionButton:
        id:update
        icon: "update"
        pos_hint:{'center_x': .85, 'center_y': .15}
        on_release:
            app.check_order(app.instance_table, app.current_row)
<Expensetable>:
    FloatLayout:
        id:expensetable
    MDFloatingActionButton:
        id:btn
        icon: "delete-circle-outline"
        pos_hint:{'center_x': .5, 'center_y': .15}
        on_release:
            app.delete_order()

    MDFloatingActionButton:
        icon: "arrow-left"
        pos_hint:{'center_x': .15, 'center_y': .15}
        on_release:
            app.change_screen('splashscreen',"nothing")
            app.welcome()

    MDFloatingActionButton:
        id:update
        icon: "update"
        pos_hint:{'center_x': .85, 'center_y': .15}
        on_release:
            app.check_expenses(app.instance_table, app.current_row)
<CustomerTable>:
    FloatLayout:
        id:customertable
    MDFloatingActionButton:
        id:btn
        icon: "delete-circle-outline"
        pos_hint:{'center_x': .5, 'center_y': .2}
        on_release:
            app.on_check_customer()
            

    MDFloatingActionButton:
        icon: "arrow-left"
        pos_hint:{'center_x': .15, 'center_y': .2}
        on_release:
            app.change_screen('splashscreen',"nothing")
            app.welcome()

    MDFloatingActionButton:
        id:update
        icon: "update"
        pos_hint:{'center_x': .85, 'center_y': .2}
        on_release:
            app.check_customer(app.instance_table, app.current_row)

"""
class HomeScreen(Screen):
    pass
class SplashScreen(Screen):
    pass

class WelcomeScreen(Screen):
    pass

class ContentNavigationDrawer(Screen):
    pass

class Content(Screen):
    pass

class Customers(Screen):
    pass
class Menu(Screen):
    pass
class UpdateMenu(Screen):
    pass
class UpdateExpenses(Screen):
    pass
class Expenses(Screen):
    pass
class AddExpense(Screen):
    pass
class Imagepreview(Screen):
    pass
class Avata(Screen):
    pass
class Order(Screen):
    pass
class Expensetable(Screen):
    pass
class CustomerTable(Screen):
    pass
class UpdateCustomer(Screen):
    pass
class UpdateOrder(Screen):
    pass


class MainApp(MDApp):
    def submit(self):
        conn = sqlite3.connect('cafe.db')
        c = conn.cursor()
        '''
        c.execute("INSERT INTO customers VALUES(:first)",
                  {
                      'first':
                  })
        '''

        conn.commit()
        conn.close()


    # Function for Convert Binary
    # Data to Human Readable Format
    def login(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Enter Password:",
                size_hint=[.5, .4],
                type="custom",
                content_cls=Imagepreview(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL", text_color=self.theme_cls.primary_color, on_release=self.closeDialog
                    ),
                    MDFlatButton(
                        text="OK", text_color=self.theme_cls.primary_color, on_release=self.post_login
                    ),
                ],
            )
        self.dialog.open()

    def build(self):
        conn = sqlite3.connect('cafe.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE if not exists customer(Name text,Phone text)""")
        c.execute("""CREATE TABLE if not exists menus_tl(name text,type text,price text)""")
        c.execute("""CREATE TABLE if not exists orders(menu text,customer text,date varchar,time varchar,status varchar)""")

        conn.commit()
        conn.close()


        screen = Builder.load_string(screen_helper)
        return screen
    dialog = None
    url = 'https://expense-manager-80787-default-rtdb.firebaseio.com/.json'
    name = StringProperty()
    price = NumericProperty()
    budget = NumericProperty()
    total_earning = NumericProperty()
    expense_image = ObjectProperty()
    remaining = NumericProperty()
    dropdown = ObjectProperty()
    today = StringProperty()
    time = StringProperty()

    data = {
        "Manage Orders": "package",
        "Add Customer": "walk",
        "Add Menu": "food-fork-drink",
        "Add Expenses": "credit-card"
    }

    def on_start(self):
        screenmanager = self.root.ids['screenmanager']
        screenmanager.current = 'welcomescreen'

    def clearoder(self):
        expense_item_list = self.root.ids['home'].ids['list']
        clear = expense_item_list
        clear.clear_widgets()
    def on_save(self, instance, value, date_range):
        start = str(date_range[0])
        end = str(date_range[-1])

        conn = sqlite3.connect('cafe.db')
        c = conn.cursor()
        query = "SELECT rowid, * FROM orders WHERE date BETWEEN ? AND ?"
        c.execute(query, (start, end))
        #c.execute("SELECT * FROM orders WHERE date=?", (priority,))
        records = c.fetchall()
        for doc in records:
            expense_item = self.root.ids['home'].ids['list']

            ite = ThreeLineAvatarIconListItem(text=str(doc[1]) + "/" + str(doc[5]),
                                              secondary_text=doc[2], tertiary_text=str(doc[0]),
                                              on_release=lambda x: self.update_status(x.tertiary_text))

            expense_item.add_widget(ite)

        conn.commit()
        conn.close()
        '''
        coll = db.collection('ORDERS')
        docs = coll.where(u'Date', u'>=', start).where(u'Date', u'<=', end).stream()
        for doc in docs:
            print(u'{} => {}'.format(doc.id, doc.to_dict()))

            expense_item = self.root.ids['home'].ids['list']

            ite = ThreeLineAvatarIconListItem(text=doc.to_dict()['Name'] + "/" + doc.to_dict()['Status'],
                                              secondary_text=doc.to_dict()['Menu'], tertiary_text=doc.id,
                                              on_release=lambda x: self.update_status(x.tertiary_text))

            expense_item.add_widget(ite)
            '''
    def onsave1(self, instance, value, date_range):
        start = str(value)
        conn = sqlite3.connect('cafe.db')
        c = conn.cursor()
        num = 5
        #c.execute("SELECT rowid, * FROM orders WHERE date = ?", (start,))
        c.execute('''\
                SELECT orders.rowid, orders.menu, orders.date, menus_tl.price
                FROM orders
                INNER JOIN menus_tl
                ON orders.menu = menus_tl.name
                WHERE orders.date = ?
                ''', (start,))
        records = c.fetchall()
        for doc in records:

            expense_item = self.root.ids['home'].ids['list']

            ite = ThreeLineAvatarIconListItem(text=str(doc[1]) + "/" + str(doc[0]),
                                              secondary_text=doc[2])

            expense_item.add_widget(ite)

        conn.commit()
        conn.close()
    def onsave(self, instance, value, date_range):
        start = str(value)
        conn = sqlite3.connect('cafe.db')
        c = conn.cursor()
        num = 5
        c.execute("SELECT rowid, * FROM orders WHERE date = ?", (start,))
        # c.execute("SELECT * FROM orders WHERE date=?", (priority,))
        records = c.fetchall()
        for doc in records:
            expense_item = self.root.ids['home'].ids['list']

            ite = ThreeLineAvatarIconListItem(text=str(doc[1]) + "/" + str(doc[5]),
                                              secondary_text=doc[2], tertiary_text=str(doc[0]),
                                              on_release=lambda x: self.update_status(x.tertiary_text))

            expense_item.add_widget(ite)

        conn.commit()
        conn.close()


        '''
        date = datetime.strptime(s, "%Y-%m-%d")
        modified_date = date + timedelta(days=1)
        sta = datetime.strftime(modified_date, "%Y-%m-%d")
        '''
    def informatic(self):
        conn = sqlite3.connect('cafe.db')
        c = conn.cursor()
        cursor = c.execute('''\
                            SELECT orders.rowid, orders.menu, orders.date, menus_tl.price,SUM(menus_tl.price) as total
                            FROM orders
                            INNER JOIN menus_tl
                            ON orders.menu = menus_tl.name
                            
                            ''')
        for row in cursor:
            print(row)
        conn.commit()
        conn.close()

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''
    def oncancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''
    def show_date_picker(self):
        date_dialog = MDDatePicker(mode="range")
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()
    def specific_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.onsave, on_cancel=self.oncancel)
        date_dialog.open()
    def specific_date_picker1(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.onsave1, on_cancel=self.oncancel)
        date_dialog.open()
    def callback(self,instance):
        if instance.icon =='walk':
            self.change_screen('customers', "add")
        elif instance.icon =='package':
            self.ORDER_TBL()
            self.change_screen('order', "add")
            self.onstart()

        elif instance.icon =='credit-card-edit':
            self.ORDER_TBL()
            self.change_screen('order', "add")
            self.onstart()

        elif instance.icon =='food-fork-drink':
            self.change_screen('menu', "add")
            self.onstart()

        elif instance.icon =='credit-card':
            self.change_screen('expenses', "add")
            self.onstart()


    def on_sta(self):
        expense_item_list = self.root.ids['home'].ids['expense_list']
        conn = sqlite3.connect('cafe.db')
        c = conn.cursor()

        c.execute("SELECT * FROM menus_tl")
        records = c.fetchall()
        conn.commit()
        conn.close()
        for doc in records:
            item = TwoLineAvatarIconListItem(text=doc[0], secondary_text=doc[1],
                                             on_release=lambda x: self.printlis(x.text))

            # icon = ImageLeftWidget(source='gardening/' + self.expense_image)
            # self.expense_image = doc.to_dict()['Image']

            # btn = MDFloatingActionButton(icon="android")
            # icn = ImageRightWidget(source= btn)
            g = doc[0]
            if g == "Rice Beans":
                src = "rice_beans.jpeg"
            elif g == "Githeri":
                src = "githeri.jpg"
            elif g == "Githeri Special":
                src = "githeri_special.jpg"
            elif g == "Rice Plain":
                src = "rice_plain.jpg"
            elif g == "Ugali Plain":
                src = "ugali_plain.jpg"
            elif g == "Ugali Mix":
                src = "ugali_mix.jpg"
            elif g == "Ugali Sukuma":
                src = "ugali_sukuma.jpg"
            elif g == "Ugali Cabbage":
                src = "ugali_cabbage.jpg"
            elif g == "Chapati":
                src = "chapati.jpg"
            elif g == "Chai":
                src = "tea.jpg"
            elif g == "Rice Ndengu":
                src = "rice_ndengu.jpg"
            elif g == "Ndengu Plain":
                src = "fries.jpg"
            elif g == "Rice Beef":
                src = "rice_beef.jpg"
            elif g == "Rice Special":
                src = "rice_special.jpg"
            elif g == "Rice Viazi":
                src = "rice_viazi.jpg"
            elif g == "Viazi":
                src = "viazi.jpg"
            elif g == "Beef":
                src = "beef.jpg"
            elif g == "Minji":
                src = "minji.jpg"
            elif g == "Rice Minji":
                src = "rice_minji.jpg"
            elif g == "cabbage":
                src = "cabbage.jpg"
            elif g == "sukuma":
                src = "sukuma.jpg"
            elif g == "Ugali Beef":
                src = "ugali_beef.jpg"
            else:
                src = "ugali_beef.jpg"
            image = ImageLeftWidget(source=src)

            # icon.add_widget(check)

            item.add_widget(image)

            self.remaining = 0
            # self.remaining = self.remaining + int(doc.to_dict()['money'])
            expense_item_list.add_widget(item)

    def lis(self):
        expense_item_lis = self.root.ids['home'].ids['expense_lis']

        conn = sqlite3.connect('cafe.db')
        c = conn.cursor()
        c.execute("SELECT * FROM customer")
        records = c.fetchall()
        conn.commit()
        conn.close()

        for doc in records:
            ite = TwoLineAvatarIconListItem(text=doc[0], secondary_text=doc[1],
                                            on_release=lambda x: self.printlist(x.text))

            expense_item_lis.add_widget(ite)




    def refreshall(self):
        #self.onstart()
        self.on_star()
        #self.onstart()
        #self.on_sta()
        #self.lis()
    def welcome(self):
        today = str(date.today())
        self.today = str(date.today())
        self.time = time.strftime("%H:%M:%S")
        self.budget = 0
        self.total_earning = 0
        conn = sqlite3.connect('cafe.db')
        c = conn.cursor()
        cursor = c.execute('''\
                    SELECT orders.rowid, orders.menu, orders.date, menus_tl.price,SUM(menus_tl.price) as total
                    FROM orders
                    INNER JOIN menus_tl
                    ON orders.menu = menus_tl.name
                    WHERE orders.date = ?
                    ''',(today,))
        for row in cursor:
            try:
                self.total_earning = (row[-1])
            except:
                self.total_earning = 0
        conn.commit()
        conn.close()

        conn = sqlite3.connect('cafe.db')
        c = conn.cursor()
        c.execute("SELECT SUM(price) as price FROM expenses")
        records = c.fetchall()
        for record in records:
            rec = record[0]
            self.budget = rec
        conn.commit()
        conn.close()

        '''
        s = start
        today = str(date.today())
        date_format = "%Y-%m-%d"
        a = datetime.strptime(s, date_format)
        b = datetime.strptime(today, date_format)
        delta = b - a
        c = (delta.days)
        '''

        expense_item_lis = self.root.ids['home'].ids['expense_lis']
        conn = sqlite3.connect('cafe.db')
        c = conn.cursor()
        c.execute("SELECT * FROM customer")
        records = c.fetchall()
        conn.commit()
        conn.close()
        # menu = db.collection(u'menu').stream()
        for doc in records:
            ite = TwoLineAvatarIconListItem(text=doc[0], secondary_text=doc[1],
                                            on_release=lambda x: self.printlist(x.text))

            expense_item_lis.add_widget(ite)
        expense_item = self.root.ids['home'].ids['list']
        '''
        orders_ref = db.collection(u'ORDERS')
        query = orders_ref.order_by(
            u'Date', direction=firestore.Query.DESCENDING).limit(50)
        orders = query.stream()
        #orders = db.collection(u'ORDERS').stream()
        for doc in orders:
            ite = ThreeLineAvatarIconListItem(text=doc.to_dict()['Name']+"/"+doc.to_dict()['Status'], secondary_text=doc.to_dict()['Menu'],tertiary_text=doc.id,
                                            on_release=lambda x: self.update_status(x.tertiary_text))

            expense_item.add_widget(ite)
        '''
        expense_item_list = self.root.ids['home'].ids['expense_list']
        conn = sqlite3.connect('cafe.db')
        c = conn.cursor()

        c.execute("SELECT * FROM menus_tl")
        records = c.fetchall()
        conn.commit()
        conn.close()
        for doc in records:
            item = TwoLineAvatarIconListItem(text=doc[0], secondary_text=doc[1],
                                             on_release=lambda x: self.printlis(x.text))

            # icon = ImageLeftWidget(source='gardening/' + self.expense_image)
            # self.expense_image = doc.to_dict()['Image']

            # btn = MDFloatingActionButton(icon="android")
            # icn = ImageRightWidget(source= btn)
            g = doc[0]
            if g == "Rice Beans":
                src = "rice_beans.jpg"
            elif g == "Githeri":
                src = "githeri.jpg"
            elif g == "Githeri Special":
                src = "githeri_special.jpg"
            elif g == "Rice Plain":
                src = "rice_plain.jpg"
            elif g == "Ugali Plain":
                src = "ugali_plain.jpg"
            elif g == "Ugali Mix":
                src = "ugali_mix.jpg"
            elif g == "Ugali Sukuma":
                src = "ugali_sukuma.jpg"
            elif g == "Ugali Cabbage":
                src = "ugali_cabbage.jpg"
            elif g == "Chapati":
                src = "chapati.jpg"
            elif g == "Chai":
                src = "tea.jpg"
            elif g == "Rice Ndengu":
                src = "rice_ndengu.jpg"
            elif g == "Ndengu Plain":
                src = "fries.jpg"
            elif g == "Rice Beef":
                src = "rice_beef.jpg"
            elif g == "Rice Special":
                src = "rice_special.jpg"
            elif g == "Rice Viazi":
                src = "rice_viazi.jpg"
            elif g == "Viazi":
                src = "viazi.jpg"
            elif g == "Beef":
                src = "beef.jpg"
            elif g == "Minji":
                src = "minji.jpg"
            elif g == "Rice Minji":
                src = "rice_minji.jpg"
            elif g == "cabbage":
                src = "cabbage.jpg"
            elif g == "sukuma":
                src = "sukuma.jpg"
            elif g == "Ugali Beef":
                src = "ugali_beef.jpg"
            else:
                src = "ugali_beef.jpg"
            image = ImageLeftWidget(source=src)

            # icon.add_widget(check)

            item.add_widget(image)

            self.remaining = 0
            # self.remaining = self.remaining + int(doc.to_dict()['money'])
            expense_item_list.add_widget(item)


    def on_star(self):
        today = str(date.today())
        self.today = str(date.today())
        self.time = time.strftime("%H:%M:%S")
        self.budget = 0
        self.total_earning = 0
        conn = sqlite3.connect('cafe.db')
        c = conn.cursor()
        cursor = c.execute('''\
                            SELECT orders.rowid, orders.menu, orders.date, menus_tl.price,SUM(menus_tl.price) as total
                            FROM orders
                            INNER JOIN menus_tl
                            ON orders.menu = menus_tl.name
                            WHERE orders.date = ?
                            ''', (today,))
        for row in cursor:
            try:
                self.total_earning = (row[-1])
            except:
                self.total_earning = 0
        conn.commit()
        conn.close()

        conn = sqlite3.connect('cafe.db')
        c = conn.cursor()
        c.execute("SELECT SUM(price) as price FROM expenses")
        records = c.fetchall()
        for record in records:
            rec = record[0]
            self.budget = rec
        conn.commit()
        conn.close()

        '''
        s = start
        today = str(date.today())
        date_format = "%Y-%m-%d"
        a = datetime.strptime(s, date_format)
        b = datetime.strptime(today, date_format)
        delta = b - a
        c = (delta.days)
        '''

        expense_item_lis = self.root.ids['splashscreen'].ids['expense_lis']
        conn = sqlite3.connect('cafe.db')
        c = conn.cursor()
        c.execute("SELECT * FROM customer")
        records = c.fetchall()
        conn.commit()
        conn.close()
        # menu = db.collection(u'menu').stream()
        for doc in records:
            ite = TwoLineAvatarIconListItem(text=doc[0], secondary_text=doc[1],
                                            on_release=lambda x: self.printlist(x.text))

            expense_item_lis.add_widget(ite)
        expense_item = self.root.ids['splashscreen'].ids['list']
        '''
        orders_ref = db.collection(u'ORDERS')
        query = orders_ref.order_by(
            u'Date', direction=firestore.Query.DESCENDING).limit(50)
        orders = query.stream()
        #orders = db.collection(u'ORDERS').stream()
        for doc in orders:
            ite = ThreeLineAvatarIconListItem(text=doc.to_dict()['Name']+"/"+doc.to_dict()['Status'], secondary_text=doc.to_dict()['Menu'],tertiary_text=doc.id,
                                            on_release=lambda x: self.update_status(x.tertiary_text))

            expense_item.add_widget(ite)
        '''
        expense_item_list = self.root.ids['splashscreen'].ids['expense_list']
        conn = sqlite3.connect('cafe.db')
        c = conn.cursor()

        c.execute("SELECT * FROM menus_tl")
        records = c.fetchall()
        conn.commit()
        conn.close()
        for doc in records:
            item = TwoLineAvatarIconListItem(text=doc[0], secondary_text=doc[1],
                                             on_release=lambda x: self.printlis(x.text))

            # icon = ImageLeftWidget(source='gardening/' + self.expense_image)
            # self.expense_image = doc.to_dict()['Image']

            # btn = MDFloatingActionButton(icon="android")
            # icn = ImageRightWidget(source= btn)
            g = doc[0]
            if g == "Rice Beans":
                src = "rice_beans.jpg"
            elif g == "Githeri":
                src = "githeri.jpg"
            elif g == "Githeri Special":
                src = "githeri_special.jpg"
            elif g == "Rice Plain":
                src = "rice_plain.jpg"
            elif g == "Ugali Plain":
                src = "ugali_plain.jpg"
            elif g == "Ugali Mix":
                src = "ugali_mix.jpg"
            elif g == "Ugali Sukuma":
                src = "ugali_sukuma.jpg"
            elif g == "Ugali Cabbage":
                src = "ugali_cabbage.jpg"
            elif g == "Chapati":
                src = "chapati.jpg"
            elif g == "Chai":
                src = "tea.jpg"
            elif g == "Rice Ndengu":
                src = "rice_ndengu.jpg"
            elif g == "Ndengu Plain":
                src = "fries.jpg"
            elif g == "Rice Beef":
                src = "rice_beef.jpg"
            elif g == "Rice Special":
                src = "rice_special.jpg"
            elif g == "Rice Viazi":
                src = "rice_viazi.jpg"
            elif g == "Viazi":
                src = "viazi.jpg"
            elif g == "Beef":
                src = "beef.jpg"
            elif g == "Minji":
                src = "minji.jpg"
            elif g == "Rice Minji":
                src = "rice_minji.jpg"
            elif g == "cabbage":
                src = "cabbage.jpg"
            elif g == "sukuma":
                src = "sukuma.jpg"
            elif g == "Ugali Beef":
                src = "ugali_beef.jpg"
            else:
                src = "ugali_beef.jpg"
            image = ImageLeftWidget(source=src)

            # icon.add_widget(check)

            item.add_widget(image)

            self.remaining = 0
            # self.remaining = self.remaining + int(doc.to_dict()['money'])
            expense_item_list.add_widget(item)
    def warning(self,*args):
        sb = Snackbar(text='Warning! Add customer to previous menu first',bg_color=(0, 0, 0, 1))
        sb.ids.text_bar.text_color = (1, 0, 0, 1)
        sb.open()

    def clearmenu(self):
        expense_item_list = self.root.ids['home'].ids['expense_list']
        clear = expense_item_list
        clear.clear_widgets()
    def onstart(self):
        expense_item_list = self.root.ids['home'].ids['expense_list']
        clear = expense_item_list
        clear.clear_widgets()
        expense_item_lis = self.root.ids['home'].ids['expense_lis']
        clear = expense_item_lis
        clear.clear_widgets()
        expense_lis = self.root.ids['home'].ids['list']
        clear = expense_lis
        clear.clear_widgets()

    def update_status(self,a):
        paid = "PAID"
        conn = sqlite3.connect('cafe.db')
        c = conn.cursor()
        c.execute("UPDATE orders SET status=? WHERE rowid=? ",
                  (paid, a))

        conn.commit()
        conn.close()
        sb = Snackbar(text='Payment Status Updated!', bg_color=(0, 0, 0, 1))
        sb.ids.text_bar.text_color = (0, 1, 0, 1)
        sb.open()
    def printlist(self,a):
        conn = sqlite3.connect('cafe.db')
        c = conn.cursor()
        c.execute("UPDATE orders SET customer=? WHERE customer=? ",
                  (a, "none"))

        conn.commit()
        conn.close()

        sb = Snackbar(text='Customer Added Successfully!', bg_color=(0, 0, 0, 1))
        sb.ids.text_bar.text_color = (0, 1, 0, 1)
        sb.open()


        #print (len(oda))
    def datformart(self):
        y = time.strftime("%d-%m-%Y")
        m= time.strftime("%H:%M:%S")
    def printlis(self,a):
        conn = sqlite3.connect('cafe.db')
        c = conn.cursor()
        name= "none"
        y = 'customer'

        c.execute("SELECT * FROM orders WHERE customer = ?", (name,))
        data = c.fetchall()
        if len(data) == 0:
            icon = "N/P"
            conn = sqlite3.connect('cafe.db')
            c = conn.cursor()
            name = "none"

            c.execute("INSERT INTO orders (menu,customer,date,time,status) VALUES(?,?,?,?,?)",
                      (a, name, time.strftime("%Y-%m-%d"), time.strftime("%H:%M:%S"), icon))
            c.execute("SELECT * FROM orders")
            records = c.fetchall()
            conn.commit()

            sb = Snackbar(text='Menu Added Successfully! Add Customer', bg_color=(0, 0, 0, 1))
            sb.ids.text_bar.text_color = (0, 1, 0, 1)
            sb.open()
        else:
            sb = Snackbar(text='Please allocate the last menu a customer first', bg_color=(0, 1, 0, 0))
            sb.ids.text_bar.text_color = (1, 0, 0, 1)
            sb.open()
        #c.execute("SELECT count(*) FROM orders where ?=?", (y, x))
        conn.commit()
        conn.close()


        #self.clearmenu()
        #self.on_star()

        '''
        doc = db.collection(u'ORDERS').document()
        doc.set({
            u'Menu': a,
            u'Name': " ",
            u'Date': datetime.datetime.now()
        })

        Snackbar(text='Always remember to add the menu first').open()
        '''
        '''
        for customer, menu in [(nim, nom)]:
            doc = db.collection(u'order').document()
            doc.set({
                u'customer_id': customer,
                u'menu_id': menu,

            })
        Snackbar(text= nim + " "+ nom + 'order added successfully').open()
'''

        '''
        coll = db.collection('ORDERS')
        docs = coll.where(u'Name', u'==', u' ').stream()
        for doc in docs:
            id1 = doc.id
            doc = db.collection(u'ORDERS').document(f'{id1}')
            doc.update({
                u'Name': a
            })

        Snackbar(text=a + " " + 'added successfully').open()
        '''
    def menu_callback(self, text_item):
        self.menu.dismiss()
        Snackbar(text=text_item).open()
    def set_item(self, text__item):
        self.root.ids['add_expense'].ids['namefield'].text = text__item
        self.menu.dismiss()
    def tabol(self):
        conn = sqlite3.connect('cafe.db')
        c = conn.cursor()
        c.execute("SELECT rowid,* FROM menus_tl")
        records = c.fetchall()
        conn.commit()
        conn.close()
        values = []
        for data in records:
            val=data[0]
            name = data[1]
            type = data[2]
            price = data[3]
            values.append((name,price,type,val))

        self.data_tables = MDDataTable(
            use_pagination=True,
            check=True,
            column_data=[("Name", dp(30)),
                         ("Price", dp(30)),
                         ("Type", dp(30)),
                         ("ID", dp(30))
                         ]
            ,
            row_data= values
            ,
            sorted_on="Type",
            sorted_order="ASC",
            elevation=2,
        )
        btn = self.root.ids['avata'].ids['btn']

        self.data_tables.bind(on_check_press=self.cal)
        screen = self.root.ids['avata'].ids['ava']
        screen.add_widget(self.data_tables)
        return screen

    def ORDER_TBL(self):
        conn = sqlite3.connect('cafe.db')
        c = conn.cursor()
        c.execute("SELECT rowid,* FROM orders")
        docs = c.fetchall()
        conn.commit()
        conn.close()
        values = []

        #docs = db.collection(u'ORDERS').stream()
        values = []
        for data in docs:
            val = data[0]
            name = data[2]
            menu = data[1]
            date = data[3]
            values.append((name,menu,date,val))

        self.data_tables = MDDataTable(
            use_pagination=True,
            check=True,
            column_data=[("Name", dp(30)),
                         ("Menu", dp(30)),
                         ("Date", dp(30)),
                         ("ID", dp(30))
                         ]
            ,
            row_data=values
            ,
            sorted_on="Type",
            sorted_order="ASC",
            elevation=2,
        )
        btn = self.root.ids['customertable'].ids['btn']
        self.data_tables.bind(on_check_press=self.on_row_press)
        self.data_tables.bind(on_check_press=self.cal_order_delete)
        screen = self.root.ids['order'].ids['ava']
        screen.add_widget(self.data_tables)
        return screen
    def EXPENSE_TBL(self):
        conn = sqlite3.connect('cafe.db')
        c = conn.cursor()
        c.execute("SELECT rowid,* FROM expenses")
        records = c.fetchall()
        conn.commit()
        conn.close()
        values = []
        for data in records:
            val = data[0]
            name = data[1]
            menu = data[3]
            duration = data[4]
            date = data[2]
            dat = data[5]

            values.append((name,menu,date,dat,duration,val))

        self.data_tables = MDDataTable(
            use_pagination=True,
            check=True,
            column_data=[
                         ("Name", dp(30)),
                         ("Price", dp(30)),
                         ("Quantity", dp(30)),
                         ("Date", dp(30)),
                         ("Duration", dp(30)),
                         ("ID", dp(30))
                         ]
            ,
            row_data=values
            ,
            sorted_on="Type",
            sorted_order="ASC",
            elevation=2,
        )
        btn = self.root.ids['customertable'].ids['btn']
        self.data_tables.bind(on_check_press=self.on_row_press)
        self.data_tables.bind(on_check_press=self.cal_order_delete)
        screen = self.root.ids['expensetable'].ids['expensetable']
        screen.add_widget(self.data_tables)
        return screen
    def tabal(self):
        conn = sqlite3.connect('cafe.db')
        c = conn.cursor()
        c.execute("SELECT rowid,* FROM customer")
        records = c.fetchall()
        conn.commit()
        conn.close()
        values = []
        for data in records:
            val=data[0]
            name = data[1]
            phone = data[2]
            values.append((name,phone,val))

        self.data_tables = MDDataTable(
            use_pagination=True,
            check=True,
            column_data=[
                         ("Name.", dp(30)),
                         ("Phone No.", dp(30)),
                         ("ID", dp(30))
                         ]
            ,
            row_data= values
            ,
            sorted_on="Type",
            sorted_order="ASC",
            elevation=2,
        )
        btn = self.root.ids['customertable'].ids['btn']
        self.data_tables.bind(on_check_press=self.on_row_press)
        self.data_tables.bind(on_check_press=self.cal)
        screen = self.root.ids['customertable'].ids['customertable']
        screen.add_widget(self.data_tables)
        return screen

    def cal(self,instance_table, current_row):
        #trip = [TRIPS_SELECTED[i] for i in range(len(TRIPS_SELECTED)) if i == TRIPS_SELECTED.index(TRIPS_SELECTED[i])]
        self.current_row = current_row[-1]
        self.instance_table = instance_table
    def cal_order_delete(self,instance_table, current_row):
        current = current_row[-1]
        TRIPS_SELECTED.append(current_row[-1])
        #trip = [TRIPS_SELECTED[i] for i in range(len(TRIPS_SELECTED)) if i == TRIPS_SELECTED.index(TRIPS_SELECTED[i])]
        self.current_row = current_row[-1]
        self.instance_table = instance_table

    def cal1(self,instance_table, current_row):
        self.customer1_tbl()
        current1 = current_row[0]
        TRIPS_SELECTED.append(current_row[0])
        #trip = [TRIPS_SELECTED[i] for i in range(len(TRIPS_SELECTED)) if i == TRIPS_SELECTED.index(TRIPS_SELECTED[i])]
        self.current_row = current_row[0]
    def cal2(self,instance_table, current_row):
        current2 = current_row[0]
        #trip = [TRIPS_SELECTED[i] for i in range(len(TRIPS_SELECTED)) if i == TRIPS_SELECTED.index(TRIPS_SELECTED[i])]
        self.customer1_tbl()

        TRIPS_SELECTED.append(current_row[0])
        #trip = [TRIPS_SELECTED[i] for i in range(len(TRIPS_SELECTED)) if i == TRIPS_SELECTED.index(TRIPS_SELECTED[i])]
        self.current_row = current_row[0]
    def on_row_press(self, instance_table, current_row):
        '''Called when a table row is clicked.'''
        pass
    def on_check_customer(self):
        for trip in TRIPS_SELECTED:
            conn = sqlite3.connect('cafe.db')
            c = conn.cursor()
            c.execute("DELETE FROM customer WHERE rowid = ?", trip)
            conn.commit()
            conn.close()
            #db.collection(u'customers').document(trip).delete()
            Snackbar(text='Items deleted successfully!').open()
            self.onstart()
            self.tabal()


    def remove_order(self):
        current = self.current_row
        conn = sqlite3.connect('cafe.db')
        c = conn.cursor()
        c.execute("DELETE FROM orders WHERE rowid = ?", [current])
        conn.commit()
        conn.close()
        #db.collection(u'ORDERS').document(trip).delete()
        Snackbar(text='Items deleted successfully!').open()
        self.ORDER_TBL()
    def delete_order(self):
        for trip in TRIPS_SELECTED:
            conn = sqlite3.connect('cafe.db')
            c = conn.cursor()
            c.execute("DELETE FROM expenses WHERE rowid = ?", [trip])
            conn.commit()
            conn.close()
            #db.collection(u'ORDERS').document(trip).delete()
            Snackbar(text='Items deleted successfully!').open()
            self.EXPENSE_TBL()
    def on_check(self):
        for trip in TRIPS_SELECTED:
            conn = sqlite3.connect('cafe.db')
            c = conn.cursor()
            c.execute("DELETE FROM menus_tl WHERE rowid = ?", [trip])
            conn.commit()
            conn.close()
            #db.collection(u'menu').document(trip).delete()
            Snackbar(text='Items deleted successfully!').open()
            self.onstart()
            self.tabol()

    def check_customer(self, instance_table, current_row):
        conn = sqlite3.connect('cafe.db')
        c = conn.cursor()
        c.execute("""SELECT * FROM customer WHERE ROWID = ?""", [current_row])
        #c.execute("SELECT * FROM customer where rowid =3")
        records = c.fetchall()
        for record in records:
            name = record[0]
            phone = record[1]
            screenmanager = self.root.ids['screenmanager']
            screenmanager.current = 'updatecustomer'

            self.root.ids['updatecustomer'].ids['customer_name'].text = name
            self.root.ids['updatecustomer'].ids['phone'].text = phone
            self.onstart()
        conn.commit()
        conn.close()
        '''
        name = doc.to_dict()['Name']
        phone = doc.to_dict()['Phone']
        screenmanager = self.root.ids['screenmanager']
        screenmanager.current = 'updatecustomer'

        self.root.ids['updatecustomer'].ids['customer_name'].text = name
        self.root.ids['updatecustomer'].ids['phone'].text = phone

        self.onstart()
        '''

    def check_order(self, instance_table, current_row):
        conn = sqlite3.connect('cafe.db')
        c = conn.cursor()
        c.execute("""SELECT * FROM orders WHERE ROWID = ?""", [current_row])
        # c.execute("SELECT * FROM customer where rowid =3")
        records = c.fetchall()
        for record in records:
            name = record[1]
            menu = record[0]
            screenmanager = self.root.ids['screenmanager']
            screenmanager.current = 'updateorder'

            self.root.ids['updateorder'].ids['customer_name'].text = name
            self.root.ids['updateorder'].ids['order'].text = menu
            self.onstart()
        conn.commit()
        conn.close()

        self.onstart()
    def check_expenses(self, instance_table, current_row):
        conn = sqlite3.connect('cafe.db')
        c = conn.cursor()
        c.execute("""SELECT * FROM expenses WHERE ROWID = ?""", [current_row])
        # c.execute("SELECT * FROM customer where rowid =3")
        records = c.fetchall()
        #doc = db.collection(u'Expenses').document(current_row).get()
        for record in records:
            name = record[0]
            price = record[2]
            quantity = record[1]
            duration = record[3]

            screenmanager = self.root.ids['screenmanager']
            screenmanager.current = 'updateexpenses'

            self.root.ids['updateexpenses'].ids['expense_name'].text = name
            self.root.ids['updateexpenses'].ids['expense_quantity'].text = quantity
            self.root.ids['updateexpenses'].ids['expense_price'].text = price
            self.root.ids['updateexpenses'].ids['duration'].text = duration
            self.onstart()
        conn.commit()
        conn.close()
    def check(self, instance_table, current_row):
        #coll = db.collection('menu')
        #doc = db.collection(u'menu').document(current_row).get()
        conn = sqlite3.connect('cafe.db')
        c = conn.cursor()
        c.execute("""SELECT * FROM menus_tl WHERE ROWID = ?""", [current_row])
        # c.execute("SELECT * FROM customer where rowid =3")
        records = c.fetchall()
        for record in records:
            name = record[0]
            type = record[1]
            price = record[2]

            screenmanager = self.root.ids['screenmanager']
            screenmanager.current = 'updatemenu'

            self.root.ids['updatemenu'].ids['menu_name'].text = name
            self.root.ids['updatemenu'].ids['menu_type'].text = type
            self.root.ids['updatemenu'].ids['menu_price'].text = price

            #self.clea_ava()
            self.onstart()

    # Sorting Methods:
    # since the https://github.com/kivymd/KivyMD/pull/914 request, the
    # sorting method requires you to sort out the indexes of each data value
    # for the support of selections.
    #
    # The most common method to do this is with the use of the builtin function
    # zip and enumerate, see the example below for more info.
    #
    # The result given by these funcitons must be a list in the format of
    # [Indexes, Sorted_Row_Data]


    def file_chooser(self,name,type,price):
        if name=="" or type=="" or price=="":
            Snackbar(text='All fields must be filled!').open()
        else:
            filechooser.open_file(on_selection=self.selected)
    def file_choose(self,name,type,price):
        if name=="" or type=="" or price=="":
            Snackbar(text='All fields must be filled!').open()
        else:
            filechooser.open_file(on_selection=self.sel)

    def selected(self,selection):
        if selection== []:
            self.change_screen('menu', "add")
            Snackbar(text='Choose an image first!').open()
        else:
            self.root.ids.imagepreview.ids.img.source = selection[0]
            self.change_screen('imagepreview', "nothing")

    def sel(self,selection):
        if selection== []:
            self.change_screen('menu', "add")
            Snackbar(text='Choose an image first!').open()
        else:
            self.root.ids.updatemenu.ids.img.source = selection[0]


    def customers(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Add Customers:",
                size_hint=[.5, .4],
                type="custom",
                content_cls=Customers(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL", text_color=self.theme_cls.primary_color, on_release=self.closeDialog
                    ),
                    MDFlatButton(
                        text="OK", text_color=self.theme_cls.primary_color, on_release=self.post_customers
                    ),
                ],
            )
        self.dialog.open()

    def menu(self):
        if not self.dialog:
            self.dialog = Popup(
                title="Delete Menu?",
                type="custom",
                buttons=[
                    MDFlatButton(
                        text="CANCEL", text_color=self.theme_cls.primary_color, on_release=self.closeDialog
                    ),
                    MDFlatButton(
                        text="OK", text_color=self.theme_cls.primary_color, on_release=self.on_check
                    ),
                ],
            )
        self.dialog.open()

    def delete_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Delete Order?",
                type="custom",
                buttons=[
                    MDFlatButton(
                        text="CANCEL", text_color=self.theme_cls.primary_color, on_release=self.closeDialog
                    ),
                    MDFlatButton(
                        text="OK", text_color=self.theme_cls.primary_color, on_release=self.delete_order
                    ),
                ],
            )
        self.dialog.open()



    '''
    for exchange, symbol, cap in [('TSX', 'WELL', 360), ('TSX', 'ENB', 87000)]:
        doc = db.collection(u'stocks').document(f'{exchange}-{symbol}')
        doc.set({
            u'exchange': exchange,
            u'symbol': symbol,
            u'cap': cap
    })
    '''
    def post_customers(self, name,phone):
        if name=="" or type=="" or phone=="":
            Snackbar(text='All fields must be filled!').open()
        else:
            name = self.root.ids['customers'].ids['name'].text
            #name = self.dialog.content_cls.ids.name.text
            phone = self.root.ids['customers'].ids['phone'].text

            conn = sqlite3.connect('cafe.db')
            c = conn.cursor()

            c.execute("INSERT INTO customer (Name,Phone) VALUES(?,?)",(name,phone))

            conn.commit()
            conn.close()

            self.root.ids['customers'].ids['name'].text = ""
            self.root.ids['customers'].ids['phone'].text = ""
            Snackbar(text='The customer has been added successfully!').open()
    def selec(self):
        selection=self.root.ids.imagepreview.ids.img.source

    def edit_menu(self):
        menu_name = self.root.ids['updatemenu'].ids['menu_name'].text
        menu_type = self.root.ids['updatemenu'].ids['menu_type'].text
        menu_price = self.root.ids['updatemenu'].ids['menu_price'].text
        #coll = db.collection('menu').stream()
        current_row = self.current_row
        conn = sqlite3.connect('cafe.db')
        c = conn.cursor()
        c.execute("UPDATE menus_tl SET name=?, type=?, price=? WHERE rowid=? ",
                  (menu_name, menu_type,menu_price,current_row))

        conn.commit()
        conn.close()

        Snackbar(text='Updated successfully').open()

    def edit_customer(self):
        customer_name = self.root.ids['updatecustomer'].ids['customer_name'].text
        phone = self.root.ids['updatecustomer'].ids['phone'].text

        current_row = self.current_row
        conn = sqlite3.connect('cafe.db')
        c = conn.cursor()
        c.execute("UPDATE customer SET Name=?, Phone=? WHERE rowid=? ",
                    (customer_name, phone, current_row))

        conn.commit()
        conn.close()


        Snackbar(text='Updated successfully').open()
    def edit_expense(self):
        name = self.root.ids['updateexpenses'].ids['expense_name'].text
        quantity = self.root.ids['updateexpenses'].ids['expense_quantity'].text
        price = self.root.ids['updateexpenses'].ids['expense_price'].text
        duration = self.root.ids['updateexpenses'].ids['duration'].text
        current_row = self.current_row

        current_row = self.current_row
        conn = sqlite3.connect('cafe.db')
        c = conn.cursor()
        c.execute("UPDATE expenses SET name=?, quantity=?, price=?, duration=? WHERE rowid=? ",
                  (name, quantity,price,duration,current_row))

        conn.commit()
        conn.close()
        Snackbar(text='Updated successfully').open()
    def edit_order(self):
        customer_name = self.root.ids['updateorder'].ids['customer_name'].text
        order = self.root.ids['updateorder'].ids['order'].text

        current_row = self.current_row
        conn = sqlite3.connect('cafe.db')
        c = conn.cursor()
        c.execute("UPDATE orders SET customer=?, menu=? WHERE rowid=? ",
                  (customer_name, order, current_row))

        conn.commit()
        conn.close()

        Snackbar(text='Updated successfully').open()

    def convertToBinaryData(filename,*args):
        # Convert digital data to binary format
        with open(filename, 'rb') as propic:
            blobData = propic.read()
        return blobData

    def post_menu(self, *args):
        #img = self.root.ids.imagepreview.ids.img.source
        menu_name = self.root.ids['menu'].ids['menu_name'].text
        menu_type = self.root.ids['menu'].ids['menu_type'].text
        menu_price = self.root.ids['menu'].ids['menu_price'].text

        for menu_name,menu_type,menu_price in [(menu_name,menu_type,menu_price)]:
                conn = sqlite3.connect('cafe.db')
                c = conn.cursor()

                c.execute(""" INSERT INTO menus_tl (name,type,price) VALUES (?, ?, ?)""",(menu_name, menu_type,menu_price))

                conn.commit()
                conn.close()

        #self.root.ids.imagepreview.ids.img.source=""
        self.root.ids['menu'].ids['menu_name'].text=""
        self.root.ids['menu'].ids['menu_type'].text=""
        self.root.ids['menu'].ids['menu_price'].text=""

    def post_expense(self, *args):
        expense_name = self.root.ids['expenses'].ids['expense_name'].text
        expense_quantity = self.root.ids['expenses'].ids['expense_quantity'].text
        expense_price = self.root.ids['expenses'].ids['expense_price'].text
        duration = self.root.ids['expenses'].ids['duration'].text
        date = time.strftime("%d-%m-%Y")

        conn = sqlite3.connect('cafe.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE if not exists expenses(name text,quantity text,price text,duration text,Date varchar)""")
        c.execute("INSERT INTO expenses (name,quantity,price,duration,date) VALUES(?,?,?,?,?)", (expense_name, expense_quantity, expense_price, duration,date))

        conn.commit()
        conn.close()


        Snackbar(text='Expense Added Successfully').open()
    def post_login(self, *args):
        pword = self.root.ids['welcomescreen'].ids['menu_name'].text
        if pword == "kenyaneats2022":
            self.on_star()
            self.change_screen('splashscreen','nothin')
        else:
            Snackbar(text='Wrong Password').open()
    def closeDialog(self, inst):
        self.dialog.dismiss()

    def change_screen(self, screename,status):
        screenmanager = self.root.ids['screenmanager']
        screenmanager.current = screename
        if status =="edit":
            self.root.ids['menu'].ids['menu_name'].text = "edit"
            self.root.ids['menu'].ids['menu_type'].text = "edit"
            self.root.ids['menu'].ids['menu_price'].text = "edit"

            #bal = users_ref.get(field_paths={'amount'}).to_dict().get('amount')
            #expenses = requests.get(self.url).json()


    def select_image(self, image, buttonobject):
        self.expense_image = image
        Snackbar(text='Image selected').open()
    def noti(self):
        Snackbar(text='Details successfully added').open()



sm = ScreenManager()

sm.add_widget(SplashScreen(name='splashscreen'))
sm.add_widget(WelcomeScreen(name='welcomescreen'))
sm.add_widget(HomeScreen(name='home'))
sm.add_widget(AddExpense(name='add_expense'))
sm.add_widget(Content(name='content'))
sm.add_widget(Customers(name='customers'))
sm.add_widget(Menu(name='menu'))
sm.add_widget(UpdateMenu(name='updatemenu'))
sm.add_widget(UpdateCustomer(name='updatecustomer'))
sm.add_widget(UpdateExpenses(name='updateexpenses'))
sm.add_widget(UpdateOrder(name='updateorder'))
sm.add_widget(Expenses(name='expenses'))
sm.add_widget(Avata(name='avata'))
sm.add_widget(Order(name='order'))
sm.add_widget(Expensetable(name='expensetable'))
sm.add_widget(CustomerTable(name='customertable'))
sm.add_widget(Imagepreview(name='Imagepreview'))
MainApp().run()
