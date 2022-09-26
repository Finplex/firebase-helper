from setuptools import setup, find_packages

setup(
   name="firebase_helper",
   author="Wyverns010",
   description="Private Python library which provides support features for firebase services.",
   packages=find_packages(),
   include_package_data=True,
   classifiers=[
       "Environment :: Desktop Environment",
       "Intended Audience :: Developers",
       "Operating System :: OS Independent"
       "Programming Language :: Python",
       "Programming Language :: Python :: 3.8",
    #    "Topic :: Internet :: WWW/HTTP",
    #    "Topic :: Internet :: WWW/HTTP :: Dynamic Content"
   ],
   python_requires='>=3.8',
   setup_requires=['setuptools-git-versioning'],
   version_config={
       "dirty_template": "{tag}",
   }
)