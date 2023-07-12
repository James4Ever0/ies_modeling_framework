根据识别到的单位 进行自动单位转换

定义不同语境 根据依赖关系自动排序

prepare three stacks:

- imminent execution stack: as final program will return
- late execution stack: checked after current statement displacement, repeat checking this until no change is detected in IES
- temporary late execution stack: put current statement to here before checking LES, then check statement inside, either put statement to IES or LES

in functional programming, variables are immutable (can only be defined once).

do not delegate the whole model to *.ies yet. use it on "fictious" models first.