from setuptools import setup

setup(
      name='yandex_dictionary',
      version='0.1.4',
      license='MIT',
      description='API yandex-dictionary python',
      packages=['yandex_dictionary'],
      author='Kovalenko Nikolay',
      author_email='kovalenko.n.r-g@yandex.ru',
      zip_safe=False,
      install_require=['requests'],
      classifiers=[
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8'
      ]
)
