"""
__author__ = 'fengjincong'
"""
from setuptools import setup, find_packages

setup(
    name='loran_hook',
    url='https://github.com/xxx/pytest-changecode',
    version='1.0',
    author="water",
    author_email='1696746432@qq.com',
    description='UTF-8',
    long_description='对pytest的钩子函数进行封装, 将logger注册和解除注册的操作嵌入到框架中',
    classifiers=[  # 分类索引 ，pip 对所属包的分类
        'Framework :: Pytest',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python :: 3.8',
    ],
    license='proprietary',
    # packages=['loran_hook'],
    packages=find_packages(),
    keywords=[
        'pytest', 'py.test', 'loran_hook',
    ],
    # 需要安装的依赖
    install_requires=[
        'pytest'
    ],
    # 入口模块 或者入口函数
    entry_points={
        'pytest11': [
            'loran_hook = loran_hook',
        ]
    },
)
