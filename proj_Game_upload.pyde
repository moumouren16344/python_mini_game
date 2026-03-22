def setup():
    global bg1,bg2,maincharacter,boss,bossBack,characterhp,enemy1,enemy2,enemy3
    global gamelevel,groundH,characterhpNum,bosshpNum,characterOrigionhpNum,energybarNum,bgwid,score,startTime
    global maincharacterW,maincharacterH,characterX,characterY,characterDirection,characterPreDirection,dodging
    global isright,isleft,isjumping,isup,invincibility,fly,bossAppearance,angle,rotationSpeed,bossX,bossY
    size(1920,1080)
    
    characterShoot()
    preDrawEnemy1()
    
    bg1 = loadImage("background1.png")
    bg2 = loadImage("background2.png")
    maincharacter = loadImage("maincharacterR.png")
    boss = loadImage("boss.png")
    bossBack = loadImage("bossback.png")
    characterhp = loadImage("characterhp.png")
    enemy1=loadImage("enemy1.png")
    enemy2=loadImage("enemy2.png")
    enemy3=loadImage("enemy3.png")
    
    groundH=860  #height of ground
    gamelevel=0  #welcome page
    
    isright=False
    isleft=False
    isjumping=False
    isup=False #if you push shift or space and not release
    
    maincharacterW=130
    maincharacterH=130
    
    bgwid=0  #the x position of background1
    characterX=200   #character position at the beginning of gameplay page
    characterY=groundH-130   #character position at the beginning of gameplay page
    characterDirection=RIGHT
    characterPreDirection=RIGHT
    dodging = False
    invincibility=False
    
    bossAppearance=False
    bosshpNum = 300  #hp number of boss
    bossX=width/2-75
    bossY=height/2-300

    angle = 0
    rotationSpeed = 2
    prebossAttack1()
    prebossAttack2()
    prebossAttack3()
    
    score=0
    characterhpNum = 8  #hp number of character
    characterOrigionhpNum=characterhpNum
    energybarNum = 50  #the length of energy bar
    startTime=0

def characterShoot():   #preparing for shooting
    global bullet,bulletX,bulletY,speed,bulletVisible,totalNum
    bulletX=[]
    bulletY=[]
    speed=100
    bulletVisible=[]
    totalNum=3
    for i in range (totalNum):
        bulletX.append(0)
        bulletY.append(0)
        bulletVisible.append(False)

def draw():
    global bgwid,bg,bossAppearance
    image(bg1,bgwid,0,width,height)  #background1
    if gamelevel == 2 and bossAppearance == False: #scrolling the background if boss is not come
        image(bg1,bgwid+width,0,width,height)
        bgwid=bgwid-2
        if bgwid<-width:
            bgwid=0
    elif gamelevel >= 2 and bossAppearance==True:
        image(bg2,0,0,width,height)
    if gamelevel == 0:  #welcome page
        image(maincharacter,width/2-130/2,groundH-130,maincharacterW,maincharacterH)
        drawButton(width/2-160,height/4,320,50,48,"START GAME")
    
    elif gamelevel == 1:  #introduction page
        image(maincharacter,200,groundH-130,maincharacterW,maincharacterH)
        drawText(500,200,64,"You need to act as this charactor who can ")
        drawText(500,264,64,"control ice magic and fight against the BOSS")
        drawText(500,328,32,"Press A and D for moving,")
        drawText(500,360,32,"mouse left to shoot the boss,")
        drawText(500,392,32,"Press shift to dodge the boss's attacks")
        drawText(500,424,32,"Press space to jump")
        drawText(500,456,32,"When you are jumping or dodging, you are invincible.")
        drawButton(1500,groundH+64,4*48/1.5,50,48,"PLAY")
    
    elif gamelevel == 2:  #gameplay page
        gameEnd()
        drawText(1600,40,32,"Your Score:"+str(score))
        drawCharacterhp()
        drawCharacterEnergybar()
        shooting()
        image(maincharacter,characterX,characterY,maincharacterW,maincharacterH)
        move()
        protectCharacter()
        if score<enemyNum1:
            drawEnemy1()
            decreaseCharacterHpEnemy1()
        elif score>=enemyNum1:
            bossAppearance=True
            shootBoss()
            drawBosshpBar()
            drawBoss()
            if bosshpNum>=200:
                bossAttack1()
            elif bosshpNum>=100:
                bossAttack2()
            elif bosshpNum>=0:
                bossAttack3()      
    
    elif gamelevel == 3: #game over lose
        drawText(300,400,150,"YOU LOSE")
        drawText(350,560,70,"Your score:"+str(score))
        drawButton(200,900,300,50,48,"Restart")
        drawButton(800,900,150,50,48,"Exit")
    
    elif gamelevel == 4: #game over win
        drawText(300,400,150,"YOU WIN")
        drawText(350,560,70,"Your score:"+str(score+10*characterhpNum))
        drawButton(200,900,300,50,48,"Restart")
        drawButton(800,900,150,50,48,"Exit")
        
def gameEnd():
    global gamelevel
    if characterhpNum<=0:
        gamelevel=3 #lose
    elif characterhpNum>=1 and bosshpNum<=0:
        gamelevel=4 #win
        
def drawButton(x,y,m,n,s,a):
    fill(102,204,255)
    rect(x,y,m,n)
    fill(0)
    textSize(s)
    text(str(a),x,y+s)
    
def drawText(x,y,s,a):
    fill(255)
    textSize(s)
    text(str(a),x,y+s)
    
def drawCharacterhp():
    for i in range (characterhpNum):
        image(characterhp,50+70*i,50,70,70)
        
def drawCharacterEnergybar():
    global energybarNum,isup
    if energybarNum<50 and isup==False:
        energybarNum=energybarNum+0.5
    for i in range (int(energybarNum)):
        fill(21,206,19)
        rect(50+5*i,130,5,30)
            
def drawBosshpBar():
    global bosshpNum
    drawText(150,985,48,"boss:")
    for i in range (int(bosshpNum)):
        if bosshpNum>=200:
            fill(10,255,10)
        elif bosshpNum>=100:
            fill(255,255,10)
        elif bosshpNum>=0:
            fill(255,10,10)
        rect(300+5*i,1000,5,40)
            
def mousePressed():
    global gamelevel,found
    if gamelevel == 0:
        if mouseX>=width/2-160 and mouseX<=width/2-160+320 and mouseY>=height/4 and mouseY<=height/4+50:
            gamelevel = 1 # switch to introduction page
    elif gamelevel == 1:
        if mouseX>=1500 and mouseX<=1500+4*48/1.5 and mouseY>=groundH+64 and mouseY<=groundH+64+50:
            gamelevel = 2  #switch to gameplay page
    elif gamelevel == 3:
        if mouseX>=200 and mouseX<=200+300 and mouseY>=900 and mouseY<=900+50:
            setup()
        if mouseX>=800 and mouseX<=800+150 and mouseY>=900 and mouseY<=900+50:
            exit()
    elif gamelevel == 4:
        if mouseX>=200 and mouseX<=200+300 and mouseY>=900 and mouseY<=900+50:
            setup()
        if mouseX>=800 and mouseX<=800+150 and mouseY>=900 and mouseY<=900+50:
            exit()

def keyPressed():
    global characterX,characterY,characterDirection,characterPreDirection\
    ,dodging,isright,isleft,isjumping,isup,invincibility,energybarNum,maincharacter,fly
    if gamelevel == 2:  #at gameplay page
        if key == "a":
            isleft=True
            characterDirection = LEFT
            if characterDirection != characterPreDirection:
                maincharacter=loadImage("maincharacterL.png")
                characterPreDirection=characterDirection
        if key == "d":
            isright=True
            characterDirection = RIGHT
            if characterDirection != characterPreDirection:
                maincharacter=loadImage("maincharacterR.png")
                characterPreDirection=characterDirection
        if key == " " and characterY == groundH-130 and energybarNum>=5:
            isjumping = True
            characterY=characterY-200
            energybarNum=energybarNum-5
            invincibility=True
            isup=True
        if keyCode == SHIFT and energybarNum>=15:  # when dodging, set dodging to true
            dodging = True
            invincibility=True
            dodge()
            isup=True
            
def keyReleased():  # reset movement
    global dodging,isleft,isright,isjumping,isup,invincibility,fly
    if keyCode == SHIFT:  
        dodging = False
        invincibility=False
        isup = False
    if key == "a":
        isleft = False
    if key == "d":
        isright = False
    if key == " ":
        isjumping = False
        invincibility=False
        isup=False
                
def dodge():   #the character can dodge and be invincible
    global characterX,characterY,energybarNum
    if gamelevel == 2 and dodging == True and energybarNum>=15:
        if characterDirection == RIGHT and keyCode == SHIFT:
            characterX = characterX + 200
            energybarNum=energybarNum-15
        elif characterDirection == LEFT and keyCode == SHIFT:
            characterX = characterX - 200
            energybarNum=energybarNum-15
            
def move():
    global characterX,characterY  #character instant position
    global energybarNum
    if isright == True and characterX<=1980-maincharacterW:
        characterX = characterX + 15
    if isleft == True and characterX>=0:
        characterX = characterX - 15
    if isup == True and energybarNum>=0.7:
        energybarNum=energybarNum-0.7
    if characterY<groundH-130:
        invincibility=True
        characterY=characterY+20
    else:
        invincibility=False
        
def shooting():
    if mousePressed:
        found=False
        for i in range (totalNum):
            if bulletVisible[i]==False and found==False:
                bulletX[i]=characterX+maincharacterW/2
                bulletY[i]=characterY+maincharacterH/2
                bulletVisible[i]=True
                found=True
    for i in range(totalNum):
        if bulletVisible[i]==True:
            if i % 10 == 0:
                fill(0)
            else:
                fill(102,204,255)
            rect(bulletX[i]-15,bulletY[i]-15,30,30)
            angle = atan2(mouseY-(characterY+maincharacterH/2), mouseX-(characterX+maincharacterW/2))
            dx = cos(angle) * speed
            dy = sin(angle) * speed
            bulletX[i]=bulletX[i]+dx
            bulletY[i]=bulletY[i]+dy
        if bulletX[i]>1920 or bulletX[i]<0 or bulletY[i]>1080 or bulletY[i]<0:
            bulletVisible[i]=False
            
def preDrawEnemy1():
    global enemyNum1,enemy1X,enemy1Y,enemy1dx,enemy1dy,enemy1Visible,enemy1bulletX,enemy1bulletY,\
    enemy1bulletoriX,enemy1bulletoriY,enemy1bulletSpeedX,enemy1bulletSpeedY,enemy1bulletVisible,totalNum1,enemyBulletNum1
    
    enemyNum1=30
    enemyBulletNum1=10*enemyNum1
    enemy1X=[]
    enemy1Y=[]
    enemy1dx=[]
    enemy1dy=[]
    enemy1Visible=[]
    enemy1bulletX=[]
    enemy1bulletY=[]
    enemy1bulletoriX=[]
    enemy1bulletoriY=[]
    enemy1bulletSpeedX=[]
    enemy1bulletSpeedY=[]
    enemy1bulletVisible=[]
    
    for i in range(enemyNum1):
        enemy1Visible.append(True)
        a=random(100,500)
        b=random(width/2,width)
        enemy1X.append(b)
        enemy1Y.append(a)
        enemy1bulletX.append(b)
        enemy1bulletY.append(a)
        enemy1bulletoriX.append(b)
        enemy1bulletoriY.append(a)
        enemy1bulletVisible.append(False)
        enemy1dx.append(random(10,20))
        enemy1dy.append(random(10,20))
        enemy1bulletSpeedX.append(random(3,6))
        enemy1bulletSpeedY.append(random(3,6))
    
def drawEnemy1():
    global enemyNum1,ememy1X,enemy1Y,enemy1dx,enemy1dy,enemy1Visible,enemy1bulletX,enemy1bulletY,enemy1bulletSpeed,enemy1bulletVisible,totalNum1,score
    found=False
    for i in range (enemyNum1):
        if enemy1bulletVisible[i]==False and found==False:
            a=random(100,500)
            b=random(width/2,width)
            enemy1X[i]=(b)
            enemy1Y[i]=(a)
            enemy1bulletX[i]=(b)
            enemy1bulletY[i]=(a)
            enemy1bulletVisible[i]=True
            found=True
    for i in range (enemyNum1):
        if enemy1Visible[i]==True:
            image(enemy1,enemy1X[i],enemy1Y[i],70,70)
            enemy1X[i]=enemy1X[i]-enemy1dx[i]
            enemy1Y[i]=enemy1Y[i]+enemy1dy[i]
            if enemy1bulletVisible[i]==True:
                fill(255,0,0)
                ellipse(enemy1bulletX[i]+35,enemy1bulletY[i]+35,30,30) #enemy1's bullets
                enemy1bulletX[i]=enemy1bulletX[i]-enemy1bulletSpeedX[i]-enemy1dx[i]
                enemy1bulletY[i]=enemy1bulletY[i]+enemy1bulletSpeedY[i]+abs(enemy1dy[i])
            if enemy1X[i]+70<0:  #if go outside
                enemy1X[i]=1920
                enemy1bulletX[i]=1920
                q=random(100,500)
                enemy1Y[i]=q
                enemy1bulletY[i]=q
                enemy1dx[i]=(random(10,20))
                enemy1dy[i]=(random(10,20))
            if enemy1Y[i]>550 or enemy1Y[i]<50: #if hit the wall
                enemy1dy[i]=-enemy1dy[i]
            if enemy1bulletX[i]<0 or enemy1bulletY[i]>1080: #if bullet go outside
                enemy1bulletX[i]=enemy1X[i]
                enemy1bulletY[i]=enemy1Y[i]
                enemy1bulletSpeedX[i]=(random(3,6))
                enemy1bulletSpeedY[i]=(random(3,6))
            for b in range(totalNum):
                for i in range (enemyNum1):
                    if bulletX[b]<enemy1X[i]+70 and bulletX[b]+30>enemy1X[i] and bulletY[b]<enemy1Y[i]+70 \
                        and bulletY[b]+30>enemy1Y[i] and enemy1Visible[i]==True and bulletVisible[b]==True:
                        enemy1Visible[i]=False
                        bulletVisible[b]=False
                        score=score+1

def decreaseCharacterHpEnemy1(): #if character is hit by the enemy1's bullets
    global characterhpNum
    for i in range (enemyNum1):
        if enemy1bulletX[i]-15<characterX+maincharacterW*3/4 and enemy1bulletX[i]+15>characterX+maincharacterW/4 \
            and enemy1bulletY[i]+15>characterY+maincharacterH/4 and enemy1bulletY[i]-15<characterY+maincharacterH*3/4 \
                and enemy1bulletVisible[i]==True and invincibility==False:
            enemy1bulletVisible[i]=False
            characterhpNum=characterhpNum-1
            
def protectCharacter(): #let the character's hp do not go down too fast
    global invincibility,characterOrigionhpNum,startTime
    if characterhpNum != characterOrigionhpNum and invincibility==False:
        invincibility=True
        characterOrigionhpNum=characterhpNum
        startTime=millis()
    if millis()-startTime>=1000 and millis()-startTime<=1500 and invincibility==True:
        invincibility=False
        
def shootBoss():
    global bulletVisible,bosshpNum,score
    for i in range (totalNum):
        if bulletX[i]<bossX+75 and bulletX[i]+30>bossX and bulletY[i]<bossY+75 and bulletY[i]+30>bossY and bossAppearance==True:
            bulletVisible[i]=False
            bosshpNum=bosshpNum-1
            score=score+1
        
def drawBoss(): #show the boss and its back patteron
    global angle
    pushMatrix() #recording the change
    translate(bossX+75,bossY+75) #set the center to boss's center
    rotate(radians(angle))
    image (bossBack,-100,-100,200,200)
    angle=angle+rotationSpeed
    popMatrix() #set back the origional center
    image (boss,bossX,bossY,150,150)
    
def prebossAttack1():
    global boss_dx1,line1X,line1Y,line1W,line1H,line1_dy,line1Visible
    boss_dx1=10  # when boss at stage1, the moveing speed of boss
    line1X=[]
    line1Y=[]
    line1W=[]
    line1H=[]
    line1_dy=[]
    line1Visible=[]
    for i in range (30):
        if i % 2==0:
            line1X.append(width/2-200)
        else:
            line1X.append(0)
        line1Y.append(0)
        line1W.append(width/2+200)
        line1H.append(10)
        line1_dy.append(5)
        line1Visible.append(False)

def bossAttack1():
    global bossX,boss_dx1,line1Visible,bosshpNum,characterhpNum
    bossX=bossX+boss_dx1
    if bossX<=300 or bossX>=1620:
        boss_dx1=-boss_dx1
    for i in range (30):
        if line1Visible[i]==False:
            if i==0 or (i>=1 and line1Y[i-1]-line1Y[i]>=300):
                line1Visible[i]=True
    for i in range(30):
        if line1Visible[i]==True:
            fill (255,0,0)
            rect(line1X[i],line1Y[i],line1W[i],line1H[i])
            line1Y[i]=line1Y[i]+line1_dy[i]
        if line1Y[i]>1080:
            line1Visible[i]=False
            line1Y[i]=line1Y[i]+line1_dy[i]
        if line1X[i]<characterX+maincharacterW*3/4 and line1X[i]+line1W[i]>characterX+maincharacterW/4 \
            and line1Y[i]<characterY+maincharacterH*3/4 and line1Y[i]+line1H[i]>characterY+maincharacterH/4 \
                and line1Visible[i]==True and invincibility==False:
                    characterhpNum=characterhpNum-1
    if line1Y[29]>1080:
        bosshpNum=199

def prebossAttack2():
    global bullet2X,bullet2oriX,bullet2oriY,bullet2Y,bullet2W,bullet2H,bullet2_dx,bullet2_dy,bullet2Visible,speed2
    global boss_dx2,boss_dy2
    bullet2X=[]
    bullet2Y=[]
    bullet2oriX=[]
    bullet2oriY=[]
    bullet2W=[]
    bullet2H=[]
    bullet2_dx=[]
    bullet2_dy=[]
    bullet2Visible=[]
    boss_dx2=5
    boss_dy2=5
    speed2=10
    for i in range (10):
        bullet2X.append(bossX)
        bullet2oriX.append(bossX)
        bullet2Y.append(bossY)
        bullet2oriY.append(bossY)
        bullet2W.append(30)
        bullet2H.append(30)
        bullet2_dx.append(3)
        bullet2_dy.append(3)
        bullet2Visible.append(False)
        
def bossAttack2():
    global bossX,bossY,boss_dx2,boss_dy2,bullet2Visible,characterhpNum
    bossX=bossX+boss_dx2
    bossY=bossY+boss_dy2
    if bossX<=400 or bossX>=1520:
        boss_dx2=-boss_dx2
    if bossY>=height/2-300+100 or bossY<=height/2-300-100:
        boss_dy2=-boss_dy2
    found=False
    for i in range (10):
        if bullet2Visible[i]==False:
            if (i==0 and found==False) or (i>=1 and ((bullet2Y[i-1]-bullet2Y[i])*(bullet2Y[i-1]-bullet2Y[i])+(bullet2X[i-1]-bullet2X[i])*(bullet2X[i-1]-bullet2X[i]))>=10000  and found==False):
                bullet2oriX[i]=bossX+75
                bullet2oriY[i]=bossY+75
                bullet2X[i]=bossX+75
                bullet2Y[i]=bossY+75
                bullet2Visible[i]=True
                found=True
    for i in range (10):
        if bullet2Visible[i]==True:
            fill (255,0,0)
            ellipse(bullet2X[i]-15,bullet2Y[i]-15,30,30)
            angle = atan2(characterY+maincharacterW/2-bullet2oriY[i], characterX+maincharacterH/2-bullet2oriX[i])
            bullet2_dx[i] = cos(angle) * speed2
            bullet2_dy[i] = sin(angle) * speed2
            bullet2X[i]=bullet2X[i]+bullet2_dx[i]
            bullet2Y[i]=bullet2Y[i]+bullet2_dy[i]
        if bullet2X[i]>1920 or bullet2X[i]<0 or bullet2Y[i]>1080 or bullet2Y[i]<0:
            bullet2Visible[i]=False
        if bullet2X[i]-15<characterX+maincharacterW*3/4 and bullet2X[i]+15>characterX+maincharacterW/4 \
            and bullet2Y[i]+15>characterY+maincharacterH/4 and bullet2Y[i]-15<characterY+maincharacterH*3/4 \
                and bullet2Visible[i]==True and invincibility==False:
                    bullet2Visible[i]=False
                    characterhpNum=characterhpNum-1
                    
def prebossAttack3():
    global line3X,line3Y,line3W,line3H,line3_dx,line3Visible
    line3X=[]
    line3Y=[]
    line3W=[]
    line3H=[]
    line3_dx=[]
    line3Visible=[]
    for i in range (30):
        line3X.append(0)
        line3Y.append(0)
        line3W.append(10)
        line3H.append(height)
        line3_dx.append(5)
        line3Visible.append(False)
        
def bossAttack3():
    global bossX,boss_dx1,line3Visible,bosshpNum,characterhpNum
    bossX=bossX+boss_dx1
    if bossX<=300 or bossX>=1620:
        boss_dx1=-boss_dx1
    for i in range (30):
        if line3Visible[i]==False:
            if i==0 or (i>=1 and line3X[i-1]-line3X[i]>=500):
                line3Visible[i]=True
    for i in range(30):
        if line3Visible[i]==True:
            fill (255,0,0)
            rect(line3X[i],line3Y[i],line3W[i],line3H[i])
            line3X[i]=line3X[i]+line3_dx[i]
        if line3X[i]>1920:
            line3Visible[i]=False
            line3X[i]=line3X[i]+line3_dx[i]
        if line3X[i]<characterX+maincharacterW*3/4 and line3X[i]+line3W[i]>characterX+maincharacterW/4 \
            and line3Y[i]<characterY+maincharacterH*3/4 and line3Y[i]+line3H[i]>characterY+maincharacterH/4 \
                and line3Visible[i]==True and invincibility==False:
                    characterhpNum=characterhpNum-1
