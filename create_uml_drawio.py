#!/usr/bin/env python3
"""
Создает базовые Draw.io файлы для всех UML диаграмм
"""

import os
from pathlib import Path

UML_DIAGRAMS = {
    # Image Processing
    'UML_IMAGE_PROCESSING_1_UseCase.drawio': 'Use Case',
    'UML_IMAGE_PROCESSING_2_Activity.drawio': 'Activity',
    'UML_IMAGE_PROCESSING_3_Sequence.drawio': 'Sequence',
    'UML_IMAGE_PROCESSING_4_Class.drawio': 'Class',
    'UML_IMAGE_PROCESSING_5_State.drawio': 'State',
    'UML_IMAGE_PROCESSING_6_Component.drawio': 'Component',
    
    # Text Analysis
    'UML_TEXT_ANALYSIS_1_UseCase.drawio': 'Use Case',
    'UML_TEXT_ANALYSIS_2_Activity.drawio': 'Activity',
    'UML_TEXT_ANALYSIS_3_Sequence.drawio': 'Sequence',
    'UML_TEXT_ANALYSIS_4_Class.drawio': 'Class',
    'UML_TEXT_ANALYSIS_5_State.drawio': 'State',
    'UML_TEXT_ANALYSIS_6_Component.drawio': 'Component',
    
    # Registration
    'UML_REGISTRATION_1_UseCase.drawio': 'Use Case',
    'UML_REGISTRATION_2_Activity.drawio': 'Activity',
    'UML_REGISTRATION_3_Sequence.drawio': 'Sequence',
    'UML_REGISTRATION_4_Class.drawio': 'Class',
    'UML_REGISTRATION_5_State.drawio': 'State',
    'UML_REGISTRATION_6_Component.drawio': 'Component',
    
    # Data Upload
    'UML_DATA_UPLOAD_1_UseCase.drawio': 'Use Case',
    'UML_DATA_UPLOAD_2_Activity.drawio': 'Activity',
    'UML_DATA_UPLOAD_3_Sequence.drawio': 'Sequence',
    'UML_DATA_UPLOAD_4_Class.drawio': 'Class',
    'UML_DATA_UPLOAD_5_State.drawio': 'State',
    'UML_DATA_UPLOAD_6_Component.drawio': 'Component',
}

def create_uml_drawio(filename, diagram_type):
    """Создает базовый Draw.io файл для UML диаграммы"""
    name = filename.replace('.drawio', '').replace('UML_', '')
    
    template = f'''<mxfile host="app.diagrams.net">
  <diagram name="{name}" id="{name.lower().replace('_', '-')}">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1200" pageHeight="800" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="2" value="{diagram_type} Diagram: {name}" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=16;fontStyle=1" vertex="1" parent="1">
          <mxGeometry x="400" y="50" width="400" height="40" as="geometry" />
        </mxCell>
        <mxCell id="3" value="UML {diagram_type} Diagram" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="300" y="300" width="400" height="200" as="geometry" />
        </mxCell>
        <mxCell id="4" value="Note: This diagram needs to be created in Draw.io based on the PlantUML source file" style="text;html=1;strokeColor=#d6b656;fillColor=#fff2cc;align=left;verticalAlign=top;whiteSpace=wrap;rounded=0;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="300" y="550" width="400" height="100" as="geometry" />
        </mxCell>
        <mxCell id="5" value="Source: diagrams-codes/{filename.replace('.drawio', '.puml')}" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=10;fontColor=#666666;" vertex="1" parent="1">
          <mxGeometry x="300" y="680" width="400" height="30" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''
    
    filepath = Path('diagrams-codes') / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(template)
    print(f"Created: {filepath}")

def main():
    """Создает все UML Draw.io файлы"""
    for filename, diagram_type in UML_DIAGRAMS.items():
        create_uml_drawio(filename, diagram_type)

if __name__ == '__main__':
    main()

