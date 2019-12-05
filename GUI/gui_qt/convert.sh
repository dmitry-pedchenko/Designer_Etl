#!/usr/bin/env bash
pyuic5 mainwindow.ui -o main_window.py -x
pyuic5 setup_db_widget.ui -o form_preferences.py -x
pyuic5 wizard_page_1.ui -o form_wizard_page_1.py -x
pyuic5 wizard_page_2.ui -o form_wizard_page_2.py -x
pyuic5 wizard_page_3.ui -o form_wizard_page_3.py -x
pyuic5 wizard_page_4.ui -o form_wizard_page_4.py -x
pyuic5 wizard_page_5.ui -o form_wizard_page_5.py -x
pyuic5 wizard_page_6.ui -o form_wizard_page_6.py -x
pyuic5 wizard_page_7.ui -o form_wizard_page_7.py -x
pyuic5 wizard_page_8.ui -o form_wizard_page_8.py -x