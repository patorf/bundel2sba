import re
import numpy as np
from cam_point_connection import cam_point_connection
from camera import Camera
from point import Point

cams = []
""":type: list of Camera"""
points = []
""":type: list of Point"""
connections = []
""":type: list of cam_point_connection"""


def loadBundlerMetaData(line):
    """

    :param line: string
    :return: (int,int)
    """
    m = re.search('(\d+) (\d+)', line)
    cams_count = int(m.group(1))
    points_count = int(m.group(2))
    return (cams_count, points_count)


def loadCam(lines):
    """

    :param lines: list[string]
    :return: Camera
    """
    current_cam = None
    for index_cam_line, line in enumerate(lines):  # the index of the camera goes from 0 to 4
        if index_cam_line == 0:
            current_cam = Camera()
            m = re.search('(.+) (.+) (.+)', line)
            current_cam.focal = float(m.group(1))
            current_cam.radialDis = np.array([float(m.group(2)), float(m.group(3))])
        elif index_cam_line == 1:
            # the rotation matrix has 3 rows
            m1 = re.search('(.+) (.+) (.+)', lines[index_cam_line])
            firstrow = np.array([float(m1.group(1)), float(m1.group(2)), float(m1.group(3))])
            current_cam.rot = firstrow
        elif index_cam_line == 2:
            m2 = re.search('(.+) (.+) (.+)', lines[index_cam_line])
            secontrow = np.array([float(m2.group(1)), float(m2.group(2)), float(m2.group(3))])
            current_cam.rot = np.vstack((current_cam.rot, secontrow))
        elif index_cam_line == 3:
            m3 = re.search('(.+) (.+) (.+)', lines[index_cam_line])
            thirdrow = np.array([float(m3.group(1)), float(m3.group(2)), float(m3.group(3))])
            current_cam.rot = np.vstack((current_cam.rot, thirdrow))
        elif index_cam_line == 4:
            m = re.search('(.+) (.+) (.+)', line)
            pos = np.array([float(m.group(1)), float(m.group(2)), float(m.group(3))])
            current_cam.pos = pos
    return current_cam


def loadPoints(pointlist, connectionlist, lines):
    """

    :param pointlist: list[Point]
    :param connectionlist: list[cam_point_connection]
    :param lines: list[string]
    """
    index_point_line = 0
    current_point = None
    while index_point_line < len(lines):
        line = lines[index_point_line]

        if index_point_line == 0:
            # first line: <X> <Y> <Z>

            current_point = Point()
            pointlist.append(current_point)
            current_point.no = len(pointlist) - 1
            m = re.search('(.+) (.+) (.+)', line)

            pos = np.array([float(m.group(1)), float(m.group(2)), float(m.group(3))])
            current_point.pos = pos
            index_point_line += 1

        elif index_point_line == 1:
            # second line: <R> <G> <B>
            m = re.search('(\d+) (\d+) (\d+)', line)

            current_point.color = np.array([int(m.group(1)), int(m.group(2)), int(m.group(3))])

            index_point_line += 1
        elif index_point_line == 2:
            # third line: <length of the list> <camera> <key> <x> <y>,
            m = re.search('(\A\d+) ', line)
            num_camPoint_connection = int(m.group(1))
            line = re.sub('(\A\d+) ', '', line)
            for j in range(num_camPoint_connection):
                m = re.search('\A(\d+)\s(\d+)\s(\S+)\s(\S+)\s', line)  # <camera> <key> <x> <y>

                connection = cam_point_connection(int(m.group(1)),
                                                  int(m.group(2)),
                                                  np.array([float(m.group(3)), float(m.group(4))]))
                connection.point_global = len(pointlist) - 1

                current_point.measured_in.append(int(m.group(1)))

                connectionlist.append(connection)

                line = re.sub('\A(\d+)\s(\d+)\s(\S+)\s(\S+)\s', '', line)

        index_point_line += 1


def load_bunler_file(filename):
    """
    load bundler file and saves its contend to points, cams an connections
    :param filename: string
    """
    cams_count = None
    points_count = None
    with open(filename) as f:
        content = f.readlines()
        index_point_line = 0  # the index of the point goes from 0 to 2
        current_cam = None
        current_point = None
        lineIndex = 0
        while lineIndex < len(content):
            # for i in range(len(content)):
            line = content[lineIndex]
            if lineIndex == 0:
                # ignore first line
                pass
            elif lineIndex == 1:
                cams_count_r, points_count_r = loadBundlerMetaData(line)
                cams_count = cams_count_r
                points_count = points_count_r
            # load all cams
            elif 1 < lineIndex < (5 * cams_count) + 2:
                # for every of the 5 lines for the cam parameter use af different regex to load the data to the object
                # in the first line the camera object is created
                current_cam = loadCam(content[lineIndex:lineIndex + 5])
                cams.append(current_cam)
                lineIndex += 4

            # load all Points and connections
            elif lineIndex > cams_count * 5 + 1:
                loadPoints(points, connections, content[lineIndex:lineIndex + 3])
                lineIndex += 2

            lineIndex += 1
        f.close()


def appendPoints2Cams():
    """
    use the connections list to store the point measurement to each cam.

    """
    for connection in connections:
        currentCamID = connection.cam
        currentPointID = connection.point_global
        cam = cams[currentCamID]
        point = points[currentPointID]
        cam.measured_points.append((point, connection.pos))


def output2_Cam_Point_Pixel(filename="output.txt"):
    """
    wire a textfile with in the format <CamID> <PointID_global> <Pixel_x> <Pixel_y>

    :param filename: string
    """
    # f = open("nordkammer.txt",'w')
    f = open(filename, 'w')

    for camID, cam in enumerate(cams):
        for point in cam.measured_points:
            pointObject = point[0]
            pointCamPos = point[1]
            outputSting = ''
            outputSting += '%-4i' % camID
            outputSting += '%-10i' % pointObject.no
            outputSting += '%15.6f%15.6f' % (pointCamPos[0], pointCamPos[1])

            f.write(outputSting + '\n')
    f.close()

def output2_Point_MeasureCount(filename="output_cc.txt"):

    f= open(filename,'w')
    for point in points:
        outputString = ''
        outputString += '%15.6f%15.6f%15.6f'% (point.x(),point.y(),point.z())
        outputString += '%5i'% len(point.measured_in)

        f.write(outputString+'\n')


load_bunler_file("bundelout-Nordkammer.out")
#load_bunler_file("bundler.out")
appendPoints2Cams()
#output2_Cam_Point_Pixel()
output2_Point_MeasureCount()

