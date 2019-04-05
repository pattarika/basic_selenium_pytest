from app.sharepoint import SharePoint

sp = SharePoint(pytest='F')
sp.login()

sp.goto_url('admin', '')
header = sp.getText('id', 'headerText1')
print('1: ', header)

title = '0_' + header + '_tmp'
sp.toolbar_action('SmtToolbarDropdownNew1', 'Site', title)
sp.create_newsite(title, title + '_desc', title + '_url')
sp.wait(5, 'SiteMgr_ObjectList1UpToParentButton_ItemImg')

# Click checkbox to delete
sp.click('id', 'TreeView1t0')
ID = sp.firstSiteCollectionID()
sp.click('id', ID)
# sp.delete_newsite(ID, title)

# Click link title to view sitting
title = sp.get_sitename(ID)
sp.click('id', sp.link_action())

if header != sp.getText('id', 'headerText1'):
    header = sp.getText('id', 'headerText1')
    print('2: ', header)
    title = '0_' + header + '_tmp'
    sp.wait(5, 'SmtToolbarDropdownNew1')
    sp.toolbar_action('SmtToolbarDropdownNew1', 'Site', title)
    sp.create_newsite(title, title + '_longdescr', title + '_longurl')

    sp.goto_url('admin', '')
    ID = sp.firstSiteCollectionID()
    sp.click('id', ID)
    # sp.delete_newsite(ID, title)
