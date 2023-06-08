# This testSuite is to run sanity test, so only positive sanity level cases needs to be added.

from tests.test_mention import TEST_Mention
import unittest

from tests.test_bookmark import TEST_Bookmark
from tests.test_locallogin import Test_Local_login
from tests.test_schedule import Test_schedule
from tests.test_home import Test_home
from tests.test_project import Test_project
from tests.test_projectlist import TEST_Projectlist
from tests.test_comment import Test_Comment
from tests.test_base import BaseTestCase

def suite():
    suite = unittest.TestSuite()
    suite.addTest(Test_Local_login('test_displayCheck'))
    suite.addTest(Test_Local_login('test_login'))
    suite.addTest(Test_home('test_displayCheck'))
    suite.addTest(Test_home('move_to_project_page'))
    suite.addTest(Test_home('move_to_schedule_page'))
    suite.addTest(Test_home('move_to_contact_admin_page'))
    suite.addTest(Test_home('move_to_guide_page'))
    suite.addTest(Test_home('move_to_notice_page'))
    suite.addTest(Test_home('move_to_cs_page'))
    suite.addTest(Test_home('test_project_card'))
    suite.addTest(Test_home('move_to_project_create'))
    suite.addTest(Test_project('test_projectCreate'))
    suite.addTest(Test_home('validate_project_in_home'))
    suite.addTest(Test_project('test_displayCheck'))
    suite.addTest(Test_project('test_projectCreate'))
    suite.addTest(Test_project('test_projectModify'))
    suite.addTest(Test_project('test_subCreate'))
    suite.addTest(Test_project('test_subCreate'))
    suite.addTest(Test_project('test_subModify'))
    suite.addTest(Test_project('test_taskCreate'))
    suite.addTest(Test_project('test_taskModify'))
    suite.addTest(TEST_Mention('test_exit_from_mention'))
    suite.addTest(TEST_Mention('test_mention_viewall'))
    suite.addTest(TEST_Mention('test_mention_filter'))
    suite.addTest(TEST_Mention('test_mention_card'))
    # suite.addTest(Test_schedule('test_displayCheck'))
    # suite.addTest(Test_schedule('test_chart_sorting'))
    # suite.addTest(Test_schedule('test_project_filtering'))
    suite.addTest(Test_Comment('test_comment_display'))
    suite.addTest(Test_Comment('test_comment_add'))
    suite.addTest(Test_Comment('test_comment_modify'))
    suite.addTest(Test_Comment('test_reply_add'))
    suite.addTest(Test_Comment('test_reply_modify'))
    suite.addTest(Test_Comment('test_reply_delete'))
    suite.addTest(Test_Comment('test_comment_delete'))
    suite.addTest(Test_project('test_allProjectDelete'))
    

    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
