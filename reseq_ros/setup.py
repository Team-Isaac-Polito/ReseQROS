from setuptools import setup

package_name = 'reseq_ros'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Team ISAAC',
    maintainer_email='team.isaac.polito@gmail.com',
    description='The ReseQROS package',
    license='aVeryGoodLicense!',
    entry_points={
        'console_scripts': [
            'movementTest = reseq_ros.movementTest:main',
            'turn_in_place = reseq_ros.turn_in_place:main',
        ],
    },
)