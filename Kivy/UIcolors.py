#main color
main_c = [  '#130217',
            '#5f0c74',
            '#BE17E8',
            '#df8bf4',
            '#f9e8fd']

red_c = [   '#170207',
            '#730c26',
            '#e8174b',
            '#f48aae',
            '#fde8ef']

green_c = [ '#021707',
            '#0c7424',
            '#17E848',
            '#8bf4a4',
            '#e8fded']

blue_c = [  '#020d17',
            '#0c4274',
            '#1783E8',
            '#8bc1f4',
            '#e8f3fd']

yellow_c = ['#171302',
            '#745f0c',
            '#E8BE17',
            '#f4df8b',
            '#fdf9e8']

white_c = [ '#ffffff',#pure bg
            '#F1F5FC',#widget bg
            '#D5DDE9',]#white outline

gray_c = [  '#A8B7CE',#bg gray
            '#7C899C',#outline gray
            '#576375',]#text gray

black_c = [ '#30343b',#bg black
            '#1A2029',]#text black

#==================#
colors = [main_c,red_c,green_c,blue_c,yellow_c,white_c,gray_c,black_c]
colorskv = []

def rgb_to_kivy(color):
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    a = int(color[7:9], 16) if len(color) == 9 else 255
    return (r/255, g/255, b/255, a/255)

for i in colors:
    array = []
    for j in i:
        array.append(rgb_to_kivy(j))
    colorskv.append(array)
#==================#
main_c   = colorskv[0]
red_c    = colorskv[1]
green_c  = colorskv[2]
blue_c   = colorskv[3]
yellow_c = colorskv[4]
white_c  = colorskv[5]
gray_c   = colorskv[6]
black_c  = colorskv[7]
transparent = (0,0,0,0)