/* eslint-disable react-hooks/exhaustive-deps */
import React from 'react';
import { Modal, Steps, Select, Typography, InputNumber } from 'antd';

const { Title } = Typography;
const { Step } = Steps;
const { Option } = Select;

export default ({
  columns,
  currentStep,
  steps,
  handleOk,
  handleCancel,
  width,
  dateVariable,
  salesVariable,
  storeIdVariable,
  itemIdVariable,
  setDateVarible,
  setSalesVariable,
  setStoreIdVariable,
  setItemIdVariable,
  monthsToPredict,
  setMonthsToPredict
}) => (
  <Modal
    visible
    onOk={handleOk}
    onCancel={handleCancel}
    width={width}
    centered
    okText="Siguiente"
    cancelText="Cancelar"
    closable={false}
  >
    <Steps size="small" current={currentStep}>
      {steps &&
        steps.length > 0 &&
        steps.map(step => <Step title={step.name} key={step.key} />)}
    </Steps>
    <div
      style={{
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        width,
        paddingTop: 50,
        paddingBottom: 30,
        paddingLeft: 30
      }}
    >
    <div style={{marginBottom:10}}>
        <Title level={4}>Fecha de venta</Title>
        <Select
          defaultValue={dateVariable}
          onChange={setDateVarible}
          style={{ width: '40%' }}
          allowClear
        >
          {columns
            .filter(
              column =>
                column.name !== itemIdVariable &&
                column.name !== storeIdVariable &&
                column.name !== salesVariable
            )
            .map(column => (
              <Option value={column.name}>{column.name}</Option>
            ))}
        </Select>
      </div>
      <div style={{marginBottom:10}}>
        <Title level={4}>Identificador de producto</Title>
        <Select
          defaultValue={itemIdVariable}
          onChange={setItemIdVariable}
          style={{ width: '40%' }}
          allowClear
        >
          {columns
            .filter(
              column =>
                column.name !== dateVariable &&
                column.name !== storeIdVariable &&
                column.name !== salesVariable
            )
            .map(column => (
              <Option value={column.name}>{column.name}</Option>
            ))}
        </Select>
      </div>
      <div style={{marginBottom:10}}>
        <Title level={4}>Identificador de sucursal</Title>
        <Select
          defaultValue={storeIdVariable}
          onChange={setStoreIdVariable}
          style={{ width: '40%' }}
          allowClear
        >
          {columns
            .filter(
              column =>
                column.name !== dateVariable &&
                column.name !== itemIdVariable &&
                column.name !== salesVariable
            )
            .map(column => (
              <Option value={column.name}>{column.name}</Option>
            ))}
        </Select>
      </div>
      <div style={{marginBottom:10}}>
        <Title level={4}>Cantidad de ventas</Title>
        <Select
          defaultValue={salesVariable}
          onChange={setSalesVariable}
          style={{ width: '40%' }}
          allowClear
        >
          {columns
            .filter(
              column =>
                column.name !== dateVariable &&
                column.name !== itemIdVariable &&
                column.name !== storeIdVariable
            )
            .map(column => (
              <Option value={column.name}>{column.name}</Option>
            ))}
        </Select>
      </div>
      <div style={{marginBottom:10}}>
        <Title level={4}>Cantidad de meses a predecir</Title>
        <InputNumber  min={1} defaultValue={monthsToPredict} onChange={setMonthsToPredict}/>
      </div>
    </div>
  </Modal>
);
