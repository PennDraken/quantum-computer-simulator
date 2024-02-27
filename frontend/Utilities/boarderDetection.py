
class BoarderDetection:
    def withinHitbox(self, width : int, height : int, xPos : int, yPos, mouseX : int, mouseY : int): 
        selectReduction = 0
        withinLowery = (yPos + (height) - selectReduction) > mouseY
        withinHighery = mouseY > yPos - (height) + selectReduction
        withinY = withinLowery and withinHighery

        withinLowerx = ( xPos - (width) + selectReduction) < mouseX
        withinHigherx = mouseX < xPos + (width) - selectReduction
        withinX = withinLowerx and withinHigherx
        return withinX and withinY

    def checkHitboxes(self, menuItems : int, boxCoordinates : [(int, int)], mouseX : int , mouseY : int ):
        print ("here")
        withinAnyHitBox = False  
        
        for i in range (0, menuItems):
            print (i)
            if self.withinHitbox(40,40,boxCoordinates[i][0],boxCoordinates[i][1], mouseX, mouseY):
                withinAnyHitBox = True
                print ("here")
                print(f"withinAnyHitBox value for iteration {i}: {withinAnyHitBox}")
        return withinAnyHitBox