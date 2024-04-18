import cv2

class FrameDrawer:
    def __init__(self):
        self.colors = {
            "Red": (0,0,255),
            "Blue": (255,0,0),
            "Green": (0,255,0),
            "Pink": (203, 192, 255),
            "Purple": (128, 0, 128),
            "Teal": (128, 128, 0),
            "Orange": (0, 165, 255),
            "Cyan": (255, 255, 0),
            "Magenta": (255, 0, 255),
            "LightBlue": (255, 229, 173),
            "Gold": (0, 215, 255), 
            "Gray": (128, 128, 128),
            "Brown": (42, 42, 165)
        }

    def drawLineFollower(self, frame, lines, color, lineSize = 2):
        for line in lines:
            linePoints = (line[0][0], line[0][1])
            self.drawLine(frame, linePoints, color, lineSize)

        return frame

    def drawSigns(self, frame, signs, colors, lineSizes):
        for i in range(len(signs)):
            for coords, sign, cont in signs[i]:
                frame = self.drawRectangles(frame, coords, colors[0], lineSize[0])
                frame = self.drawContours(frame, cont, color[1], lineSize[1])
                textOrigin = (coords[0], coords[1] + coords[3] +20)
                frame = self.drawTexts(frame, sign, textOrigin, color[2], lineSize[2])

        return frame

    def drawText(self, frame, texts, position, color, fontSize = 0.7, lineSize = 2):
        cv2.putText(frame, text, position, cv2.FONT_HERSHEY_SIMPLEX, fontSize, self.colors.get(color), lineSize)

        return frame

    def drawContour(self, frame, contours, color, lineSize = 2):
        cv2.drawContours(frame, [contour], -1, self.colors.get(color), lineSize)
        
        return frame

    def drawRectangles(self, frame, rectangle, color, lineSize = 2):
        startPoint = (rectangle[0], rectangle[1])
        endPoint = (rectangle[0] + rectangle[2], rectangle[1] + rectangle[3])
        cv2.rectangle(frame, startPoint, endPoint, self.colors.get(color), lineSize)

        return frame

    def drawLine(self, frame, line, color, lineSize = 2):
        cv2.line(frame, line[0], line[1], self.colors.get(color), lineSize)

        return frame