#/usr/bin/env python

from svgfig import *
import sys
import argparse

class PatternMaker:
  def __init__(self, cols,rows,output,units,square_size,page_width,page_height):
    self.cols = cols
    self.rows = rows
    self.output = output
    self.units = units
    self.square_size = square_size
    self.width = page_width
    self.height = page_height
    self.g = SVG("g") # the svg group container
    
  def makeCirclesPattern(self):
    spacing = self.square_size
    r = spacing / 5.0 #radius is a 5th of the spacing TODO parameterize
    c_margin = (self.width - (self.cols + 1) * spacing) / 2
    r_margin = (self.height - (self.rows + 1) * spacing) / 2
    for x in range(1,self.cols+1):
      for y in range(1,self.rows+1):
        dot = SVG("circle", cx=x * spacing + c_margin, cy=y * spacing + r_margin, r=r, fill="black", stroke="none")
        self.g.append(dot)

  def makeACirclesPattern(self):
    spacing = self.square_size
    r = spacing / 5.0
    c_margin = (self.width - (self.cols -1) * spacing) / 2
    r_margin = (self.height - (self.rows -1) * spacing) / 2
    for i in range(0,self.cols):
      for j in range(0,self.rows):
        if ((i+j)% 2): # similar to checkerboard
          dot = SVG("circle", cx=(i) * spacing + c_margin, cy=(j) * spacing + r_margin, width=spacing, height=spacing, r=r, fill="black", stroke="none")
          #dot = SVG("circle", cx= ((j*2 + i%2)*spacing) + spacing , cy=self.height - (i * spacing + spacing) , r=r, fill="black")
          self.g.append(dot)

  def makeCheckerboardPattern(self):
    spacing = self.square_size
    # center the pattern in the middle of the page
    c_margin = float( (self.width - (self.cols + 1) * spacing) / 2 )
    r_margin = float( (self.height - (self.rows + 1) * spacing) / 2 )
    #print c_margin, r_margin
    for i in range(0,self.cols + 1): # we need to draw internal corners
      for j in range(0,self.rows + 1):
        if ((i+j)% 2):
          dot = SVG("rect", x=(i) * spacing + c_margin, y=(j) * spacing + r_margin, width=spacing, height=spacing, fill="black", stroke="none")
          self.g.append(dot)

  def save(self):
    c = canvas(self.g,width="%d%s"%(self.width,self.units),height="%d%s"%(self.height,self.units),viewBox="0 0 %d %d"%(self.width,self.height))
    c.inkview(self.output)


#def makePattern(cols,rows,output,p_type,units,square_size,page_width,page_height):
#    width = page_width
#    spacing = square_size
#    height = page_height
#    r = spacing / 5.0
#    g = SVG("g") # the svg group container
#    for x in range(1,cols+1):
#      for y in range(1,rows+1):
#        if "circle" in p_type:
#          dot = SVG("circle", cx=x * spacing, cy=y * spacing, r=r, fill="black")
#        g.append(dot)
#    c = canvas(g,width="%d%s"%(width,units),height="%d%s"%(height,units),viewBox="0 0 %d %d"%(width,height))
#    c.inkview(output)


def main():
    # parse command line options
    parser = argparse.ArgumentParser(description=("Script to generate optical calibration patterns."
                                                  " Currently supported are checkerboard, circles and assymetrical "
                                                  " circles calibration targets."))
    parser.add_argument("type", choices=['circles', 'acircles', 'checkerboard'], help="Calibration target type." )
    parser.add_argument("-o", "--output",default = 'out.svg', help="Pattern save file.  Default: out.svg")
    
    
    group_r_c= parser.add_argument_group("arrangement of markers")
    group_r_c.add_argument("-s", "--spacing", type=int, help="Spacing between rows and columns of calibration points. In case of 'checkerboard' pattern spacing is is equal to square size.")
    group_r_c.add_argument("-r","--rows", type=int, default = 8)
    group_r_c.add_argument("-c","--columns", type=int, default = 6)
    
    group_size= parser.add_argument_group("pre-defined paper sizes")
    group_size.add_argument("-p", "--paper_type", choices=['letter', 'a4', 'a3'], default = 'a4', help="Note: Using the predefined sizes, units are automatically reset to mm.  Default: ISO A4")
    
    group_w_h= parser.add_argument_group("custom paper size definition")
    group_w_h.add_argument("-u", "--units", choices=['mm', 'cm', 'in'], default = 'mm', help="Default:  mm")
    group_w_h.add_argument("-W", "--page_width",type=float)
    group_w_h.add_argument("-H", "--page_height",type=float)

    args=parser.parse_args()
    
    # Choose used paper size 
    paper_sizes={"us":['mm',216,279],"a4":['mm',210,297],"a3":['mm',297,420]}
    if not (args.page_width and args.page_height):
        [args.units,args.page_width,args.page_height]=paper_sizes[args.paper_type]
        print "\nGenerating calibration pattern\n"  
        print "Paper size   : ", args.paper_type
        
    # If circle or square spacing is not defined, calculate it to fit page dimensions
    if not args.spacing:
        if (args.type == 'checkerboard'): # small hack to correctly arrange the checkerboard pattern
            w_spacing = math.floor(args.page_width * 0.95 / (args.columns+1))
            h_spacing = math.floor(args.page_height * 0.95 / (args.rows+1))
        else:
            w_spacing = math.floor(args.page_width / (args.columns))
            h_spacing = math.floor(args.page_height / (args.rows))
        args.spacing= min(w_spacing, h_spacing)
        print "Spacing      : ", args.spacing, args.units
    
    print "Rows         : ", args.rows
    print "Columns      : ", args.columns

    pm = PatternMaker(args.columns,args.rows,args.output,args.units,args.spacing,args.page_width,args.page_height)
    #dict for easy lookup of pattern type
    mp = {"circles":pm.makeCirclesPattern,"acircles":pm.makeACirclesPattern,"checkerboard":pm.makeCheckerboardPattern}
    mp[args.type]()
    # save pattern to output
    pm.save()
    print "Saved as     : ", args.output
    
if __name__ == "__main__":
    main()
    
