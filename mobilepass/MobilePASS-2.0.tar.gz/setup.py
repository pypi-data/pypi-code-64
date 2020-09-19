from setuptools import setup, find_packages
import mobilepass


setup(
    name='MobilePASS',
    version=mobilepass.__version__,
    maintainer='Raman Antanevich',
    maintainer_email='r.antanevich@ya.ru',
    url='https://github.com/rantanevich/MobilePASSER',
    description='It generates OTP based on activation code from SafeNet MobilePASS.',
    packages=find_packages(),
    test_suite='test_mobilepass',
    entry_points={
        'console_scripts': ['mobilepass = mobilepass.core:main']
    }
)