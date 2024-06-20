import cv2

class Categorization:
    def __init__(self):
        # Categories (number of points, color)
        redTriangles = (3, "red", "red triangle")
        stopSign = (8, "red", "stop sign")
        mandatory = ("circle", "blue", "mandatory sign")
        priorityRoad = (4, "yellow", "priority sign")
        prohibitory = ("circle", "red", "prohibitory sign")

        self.categories = (redTriangles, stopSign, mandatory, priorityRoad, prohibitory)


    def __del__(self):
        pass

    def findAllContours(self, mask):
        contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        app = []

        if len(contours) != 0:
            for cnt in contours:
                area = cv2.contourArea(cnt)

                if area > 1500:
                    epsilon = 0.03
                    closedPerimeter = True
                    perimeter = cv2.arcLength(cnt, closedPerimeter)
                    approx = cv2.approxPolyDP(cnt, epsilon * perimeter, closedPerimeter)
                    app.append(approx)

            return app

        return None

    def findShapes(self, app, color):
        signs = []

        # for i in range(len(app)):
            # x, y, w, h = cv2.boundingRect(app[i])

            # if len(app[i]) == 8 and contArea[i] > 1500 and color == "Red":
            #     signs.append(((x, y, w, h), "Stop", app[i]))

            # elif len(app[i]) == 3 and contArea[i] > 600 and color == "Red":
            #     signs.append(((x, y, w, h), "Yield", app[i]))

            # elif len(app[i]) == 4 and contArea[i] > 1500 and color == "Blue":
            #     signs.append(((x, y, w, h), "Pedestrian", app[i]))

            # elif len(app[i]) == 4 and contArea[i] > 1500 and color == "Yellow":
            #     signs.append(((x - 10, y - 10, w + 20, h + 20), "Priority", app[i]))

        for category in self.categories:
            if category[1] == color:
                for cont in app:
                    if len(cont) == category[0]:
                        x, y, w, h = cv2.boundingRect(cont)
                        boundingRectangle = (x - 10, y - 10, w + 20, h + 20)
                        signs.append((boundingRectangle, category[2], cont))
        
        return signs

    def categorizeSigns(self, mask, color):
        app = self.findAllContours(mask)
        signs = None

        if app is not None:
            signs = self.findShapes(app, color)

        return signs