from sharepoint import SharePoint


sp = SharePoint('firefox', 'account.txt')
sp.login('pwongcha')

sp.goto_url('admin', '')
ID = sp.firstSiteCollectionID()
title = sp.get_sitename(ID)
sp.click('id', sp.link_action())

header = sp.getText('id', 'headerText1')
print('1: ', header)

title = '0_' + header + '_tmp'
sp.toolbar_action('SmtToolbarDropdownNew1', 'Site', title)
sp.create_newsite(title, title + ' long description', title + ' long url')
sp.wait(5, 'SiteMgr_ObjectList1UpToParentButton_ItemImg')

sp.click('id', 'TreeView1t0')
# ID = sp.firstSiteCollectionID()
# sp.click('id', ID)
# # sp.delete_newsite(ID, title)

if header != sp.getText('id', 'headerText1'):
    header = sp.getText('id', 'headerText1')
    print('2: ', header)
    title = '0_' + header + '_tmp'
    sp.wait(5, 'SmtToolbarDropdownNew1')
    sp.toolbar_action('SmtToolbarDropdownNew1', 'Site', title)
    sp.create_newsite(title, title + ' long description', title + ' long url')

    sp.goto_url('admin', '')
    ID = sp.firstSiteCollectionID()
    sp.click('id', ID)
#     # sp.delete_newsite(ID, title)
