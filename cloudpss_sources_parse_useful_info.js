const {excelMap,equipmentParamDict,commonEconomicParams,specialEquipmentParamDict,equipmentParamDict2} = require("./sources")

// just do this! save this to file.

const fs = require('fs');
var object = {excelMap,equipmentParamDict,commonEconomicParams,specialEquipmentParamDict,equipmentParamDict2};
var content = JSON.stringify(object)
fs.writeFileSync(`./cloudpss_inputs.json`, content)