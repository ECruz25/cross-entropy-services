import React, { useState, Fragment, useEffect } from 'react';
import { ExcelRenderer } from 'react-excel-renderer';
import { Button } from 'antd';
import ExcelLoaderControl from './ExcelLoaderControl';
import InventoryDemandVariablePicker from './InventoryDemandVariablePicker';
import Predicting from './Predicting';
import moment, { isMoment } from 'moment';

const steps = [
  { key: 0, name: 'Seleccion de prediccion' },
  { key: 1, name: 'Seleccion de datos' },
  { key: 2, name: 'Seleccion de variables' },
  { key: 3, name: 'Prediccion de demanda' }
];

const modalWidth = 800;

const getJsDateFromExcel = excelDate => {
  const tryMoment = moment(
    new Date((excelDate - (25567 + 1)) * 86400 * 1000)
  ).format('L');
  if (!moment(new Date((excelDate - (25567 + 1)) * 86400 * 1000)).isValid()) {
    return excelDate;
  }
  return tryMoment;
};

export default () => {
  const [data, setData] = useState([]);
  const [dateVariable, setDateVarible] = useState('');
  const [salesVariable, setSalesVariable] = useState('');
  const [storeIdVariable, setStoreIdVariable] = useState('');
  const [itemIdVariable, setItemIdVariable] = useState('');
  const [currentStep, setCurrentStep] = useState(1);
  const [columns, setColumns] = useState([]);
  const [monthsToPredict, setMonthsToPredict] = useState(3);
  const [isDataTransformationDone, setIsDataTransformationDone] = useState(false);
  const [isModelTrainingStarted, setIsModelTrainingStarted] = useState(false);
  const [isModelTrainingDone, setIsModelTrainingDone] = useState(false);

  useEffect(() => {
    if (dateVariable && currentStep === 3) {
      const setDateInData = data.map(row => ({
        ...row,
        date: getJsDateFromExcel(row[dateVariable])
      }));
      debugger;
      setData(setDateInData);
    }
  }, [currentStep, dateVariable]);

  useEffect(() => {
    if (currentStep === 3) {
      handleSendDataRecollection();
    }
  }, [currentStep]);

  useEffect(() => {
    if (data.length > 0) {
      const newColumns = Object.keys(data[0]).map(t => ({
        title: t,
        dataIndex: t,
        key: t
      }));
      setColumns(newColumns);
    }
  }, [data]);

  const start = () => {
    setCurrentStep(1);
  };

  const fileHandler = event => {
    let fileObj = event.target.files[0];
    ExcelRenderer(fileObj, (err, resp) => {
      if (err) {
        console.log(err);
      } else {
        const dataColumns = resp.rows[0].map((col, index) => ({
          name: col,
          index: index + 1,
          title: col,
          dataIndex: col,
          key: col
        }));
        resp.rows.shift();
        const dataRows = resp.rows.map(row =>
          Object.assign(
            {},
            ...dataColumns.map(column => ({
              [column.name]: row[column.index - 1]
            }))
          )
        );
        setData(dataRows);
        setColumns(dataColumns);
      }
    });
  };

  const handleOk = () => {
    setCurrentStep(currentStep + 1);
  };

  const handleCancel = () => {
    setCurrentStep(currentStep - 1);
  };

  const handleSendDataRecollection = async () => {
    const request = {
      data: data.map(row => ({
        item: row[itemIdVariable],
        sales: row[salesVariable],
        date: row[dateVariable],
        store: row[storeIdVariable]
      })),
      monthsToPredict
    };
    const response = await fetch('/api/inventory-demand/data-transformation', {
      headers: { 'Content-type': 'application/json' },
      method: 'POST',
      body: JSON.stringify(request)
    });
    setIsDataTransformationDone(true);
    setIsModelTrainingStarted(true);
  };

  const renderSteps = () => {
    switch (currentStep) {
      case 0:
        return <Button onClick={start}>Empezar</Button>;
      case 1:
        return (
          <ExcelLoaderControl
            steps={steps}
            currentStep={currentStep}
            handleOk={handleOk}
            handleCancel={handleCancel}
            columns={columns}
            fileHandler={fileHandler}
            data={data}
            width={modalWidth}
          />
        );
      case 2:
        return (
          <InventoryDemandVariablePicker
            columns={columns}
            steps={steps}
            currentStep={currentStep}
            handleOk={handleOk}
            handleCancel={handleCancel}
            width={modalWidth}
            dateVariable={dateVariable}
            salesVariable={salesVariable}
            storeIdVariable={storeIdVariable}
            itemIdVariable={itemIdVariable}
            setDateVarible={setDateVarible}
            setSalesVariable={setSalesVariable}
            setStoreIdVariable={setStoreIdVariable}
            setItemIdVariable={setItemIdVariable}
            monthsToPredict={monthsToPredict}
            setMonthsToPredict={setMonthsToPredict}
          />
        );
      case 3:
        return (
          <Predicting
            columns={columns}
            steps={steps}
            currentStep={currentStep}
            handleOk={handleOk}
            handleCancel={handleCancel}
            width={modalWidth}
            isDataTransformationDone={isDataTransformationDone}
            isDataTransformationStarted={true}
            isModelTrainingDone={isModelTrainingDone}
            isModelTrainingStarted={isModelTrainingStarted}
          />
        );
      default:
        break;
    }
  };

  return <Fragment>{renderSteps()}</Fragment>;
};
