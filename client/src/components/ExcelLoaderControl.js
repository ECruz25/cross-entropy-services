import React from 'react';
import { Modal, Steps } from 'antd';
import TableControl from './TableControl';
const { Step } = Steps;

const ExcelLoader = ({
  handleOk,
  handleCancel,
  steps,
  currentStep,
  columns,
  fileHandler,
  data,
  width
}) => {
  return (
    <Modal
      visible
      onOk={handleOk}
      onCancel={handleCancel}
      width={width}
      centered
      okText="Siguiente"
      cancelText="Cancelar"
      okButtonProps={{ disabled: data.length === 0 }}
      closable={false}
    >
      <Steps size="small" current={currentStep}>
        {steps &&
          steps.length > 0 &&
          steps.map(step => <Step title={step.name} key={step.key} />)}
      </Steps>
      <input
        type="file"
        onChange={fileHandler}
        style={{ padding: '10px' }}
        accept=".csv, .xls, .xlsx"
      />
      {data && data.length > 0 && (
        <TableControl data={data} columns={columns} />
      )}
    </Modal>
  );
};

export default ExcelLoader;
