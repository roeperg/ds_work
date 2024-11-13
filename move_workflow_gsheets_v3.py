import os
import sys


baseinput = r"""    <Node ToolID="__NODE__">
      <GuiSettings Plugin="AlteryxBasePluginsGui.DbFileInput.DbFileInput">
        <Position x="__X__" y="__Y__" />
      </GuiSettings>
      <Properties>
        <Configuration>
          <Passwords />
          <File OutputFileName="" RecordLimit="" SearchSubDirs="False" FileFormat="25">C:\Users\groeper\Development\Daily\__WORKBOOK__.xlsx|||__WORKSHEET__</File>
          <FormatSpecificOptions>
            <FirstRowData>False</FirstRowData>
            <ImportLine>1</ImportLine>
          </FormatSpecificOptions>
        </Configuration>
        <Annotation DisplayMode="0">
         <DefaultAnnotationText>__WORKBOOK__.xlsx   Sheet __WORKSHEET__</DefaultAnnotationText>
          <Left value="False" />
        </Annotation>
        <Dependencies>
          <Implicit />
        </Dependencies>
        <MetaInfo connection="Output">
          <RecordInfo/>
        </MetaInfo>
      </Properties>
      <EngineSettings EngineDll="AlteryxBasePluginsEngine.dll" EngineDllEntryPoint="AlteryxDbFileInput" />
    </Node>
"""
baseoutput = r"""    <Node ToolID="__NODE__">
      <GuiSettings Plugin="AlteryxBasePluginsGui.DbFileOutput.DbFileOutput">
        <Position x="__X__" y="__Y__" />
      </GuiSettings>
      <Properties>
        <Configuration>
          <File MaxRecords="" FileFormat="25">C:\Users\groeper\Development\Daily\__WORKBOOK__.xlsx|||__WORKSHEET__</File>
          <Passwords />
          <Disable>False</Disable>
          <FormatSpecificOptions>
            <PreserveFormat>False</PreserveFormat>
            <UNCLocal>False</UNCLocal>
            <SkipFieldNames>False</SkipFieldNames>
            <OutputOption>Overwrite</OutputOption>
          </FormatSpecificOptions>
          <MultiFile value="False" />
        </Configuration>
        <Annotation DisplayMode="0">
          <Name />
          <DefaultAnnotationText>__WORKBOOK__.xlsx   Sheet __WORKSHEET__</DefaultAnnotationText>
          <Left value="False" />
        </Annotation>
        <Dependencies>
          <Implicit />
        </Dependencies>
      </Properties>
      <EngineSettings EngineDll="AlteryxBasePluginsEngine.dll" EngineDllEntryPoint="AlteryxDbFileOutput" />
    </Node>
"""

file = sys.argv[1]
with open (file, "r") as f:
	contents = f.readlines()

inq = False

output = ""

x = 100
y = 3500

targets = {}
nesting = 0
node = ""
direction = ""
myx = ""
myy = ""
workbookname = "UNKNOWN"
worksheetname = "UNKNOWN"

INGOOGLE = False


"""
<GuiSettings Plugin="Google Sheets Output">
              <Value name="workbookName">COUPAERRLOG</Value>
              <Value name="worksheetName">Sheet1</Value>
"""

for foo in range(len(contents)):
	if contents[foo].find('<Node ToolID') > -1:
		asp = contents[foo].split('"')
		nesting += 1
		nodenbr = asp[1]

	if contents[foo].find('</Node') > -1:
		if INGOOGLE:
			targets[thisnodenbr] = [workbookname,worksheetname,direction,myx,myy]
			#targets[thisnodenbr].append()
		nesting -= 1
		INGOOGLE = False

	if contents[foo].find('<GuiSettings Plugin="Google Sheets Output">') > -1:
		thisnodenbr = nodenbr
		direction = "output"
		INGOOGLE = True
		
	if contents[foo].find('<GuiSettings Plugin="Google Sheets Input">') > -1:
		thisnodenbr = nodenbr
		direction = "input"
		INGOOGLE = True

	if contents[foo].find('<Value name="workbookName">') > -1:
		dao = contents[foo].split('>')
		workbookname = dao[1].split(">")[0].split("<")[0]
		
	if contents[foo].find('<Value name="worksheetName">') > -1:
		dao = contents[foo].split('>')
		worksheetname = dao[1].split(">")[0].split("<")[0]

	if contents[foo].find('<Position x=') > -1:
		dao = contents[foo].split('"')
		myx = dao[1]
		myy = dao[3]


foo = 0
max = len(contents)

while foo < max:
	print ("TOP OF LOOP", foo)
	if contents[foo].find('<Node ToolID') > -1:
		#  FROM HERE
		asp = contents[foo].split('"')
		nesting += 1
		nodenbr = asp[1]
		if nodenbr in targets.keys():
			print(f"I will be replacing {nodenbr}  workbook {targets[nodenbr][0]} ||| {targets[nodenbr][1]} with {targets[nodenbr][2]}")
			if targets[nodenbr][2] == "input":
				#output += baseinput.replace("__NODE__", nodenbr).replace("__WORKBOOK__",targets[nodenbr][0]).replace("__WORKSHEET__",targets[nodenbr][1]).replace("__X__",targets[nodenbr][3]).replace("__Y__",targets[nodenbr][4])
				output += baseinput.replace("__NODE__", nodenbr).replace("__WORKBOOK__",targets[nodenbr][0]).replace("__WORKSHEET__",targets[nodenbr][1]).replace("__X__",str(x)).replace("__Y__",str(y))
				x += 120
			else:
				#output += baseinput.replace("__NODE__", nodenbr).replace("__WORKBOOK__",targets[nodenbr][0]).replace("__WORKSHEET__",targets[nodenbr][1]).replace("__X__",targets[nodenbr][3]).replace("__Y__",targets[nodenbr][4])
				output += baseoutput.replace("__NODE__", nodenbr).replace("__WORKBOOK__",targets[nodenbr][0]).replace("__WORKSHEET__",targets[nodenbr][1]).replace("__X__",str(x)).replace("__Y__",str(y))
				x += 120
			while contents[foo].find("</Node") == -1:
				foo += 1
			print( f"<GREG>{foo}\n")
		else:
			output += contents[foo]		
	else:
		output += contents[foo]		
	foo += 1
print(targets.keys())	
	
with open("test3.yxmd","w") as f:
	f.write(output)
	


