import os
import re
from oeqa.oetest import oeRuntimeTest


class SanityTestPython(oeRuntimeTest):

    apprt_test_python_helloworld = 'apprt_test_python_helloworld.py'
    apprt_test_python_file = 'apprt_test_python_file.py'
    apprt_test_python_stdout = 'apprt_test_python_stdout.py'

    apprt_test_python_helloworld_target = '/tmp/%s' % \
                                        apprt_test_python_helloworld
    apprt_test_python_file_target = '/tmp/%s' % apprt_test_python_file
    apprt_test_python_stdout_target = '/tmp/%s' % apprt_test_python_stdout
    apprt_apprt_test_python_file_gen = '/tmp/apprt_test_python_file.python'

    def setUp(self):
        '''
        Copy all necessary files for test to the target device. 
        '''
        self.target.copy_to(
            os.path.join(
                os.path.dirname(__file__),
                'files',
                SanityTestPython.apprt_test_python_helloworld),
            SanityTestPython.apprt_test_python_helloworld_target)
        self.target.copy_to(
            os.path.join(
                os.path.dirname(__file__),
                'files',
                SanityTestPython.apprt_test_python_file),
            SanityTestPython.apprt_test_python_file_target)
        self.target.copy_to(
            os.path.join(
                os.path.dirname(__file__),
                'files',
                SanityTestPython.apprt_test_python_stdout),
            SanityTestPython.apprt_test_python_stdout_target)


    def test_python_exists(self):
        '''
        Test if the python executable is installed and in PATH.
        '''
        (status, _) = self.target.run('which python')
        self.assertEqual(
            status,
            0,
            msg='python binary not in PATH or on target.')


    def test_python_version(self):
        '''
        Test if the version of Python is OK.
        The expected version of Python must be greater than or equal to 2.7
        '''
        (status, output) = self.target.run('python -V')
        self.assertEqual(
            status,
            0,
            msg = 'V option for python command is invalid or '\
                    'python binary does not work.')
        (_, ver) = re.split('\s+', output.strip())
        (major, minor, _) = re.split('\.', ver.strip())
        self.assertTrue(
            (major > 2) or (
                major == 2 and minor >= 7),
            msg='Python version is lower than 2.7!')


    def test_python_file(self):
        '''
        Test if files can be generated via Python code.
        '''
        (status, output) = self.target.run('python %s' %
                             SanityTestPython.apprt_test_python_file_target)
        self.assertEqual(status, 0, msg='Python test file generate failed.')
        self.assertEqual(
            output,
            SanityTestPython.apprt_apprt_test_python_file_gen,
            msg='/tmp/apprt_test_python_file.python generate failed!')


    def test_python_stdout(self):
        '''
        Test if standard output in Python works well.
        '''
        (status, output) = self.target.run('python %s' %
                        SanityTestPython.apprt_test_python_stdout_target)
        self.assertEqual(
            status,
            0,
            msg='Exit status was not 0. Output: %s' %
            output)
        self.assertEqual(
            output,
            'the value of a is 0.01',
            msg='Incorrect output: %s' %
            output)


    def test_python_helloworld(self):
        '''
        Test if the simple hello world program of Python works well.
        '''
        (status, output) = self.target.run('python %s' %
                    SanityTestPython.apprt_test_python_helloworld_target)
        self.assertEqual(
            status,
            0,
            msg='Exit status was not 0. Output: %s' %
            output)
        self.assertEqual(
            output,
            'Hello World!',
            msg='Incorrect output: %s' %
            output)


    def tearDown(self):
        '''
        Clean work: remove all the files copied to the target device.
        '''
        self.target.run(
            'rm -f %s %s %s %s' %
            (SanityTestPython.apprt_test_python_helloworld_target,
             SanityTestPython.apprt_test_python_file_target,
             SanityTestPython.apprt_test_python_stdout_target,
             SanityTestPython.apprt_apprt_test_python_file_gen))
