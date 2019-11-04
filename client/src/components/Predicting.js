import React from 'react';
import { Modal, Card, Spin, Icon, Progress } from 'antd';

export default ({
  handleOk,
  handleCancel,
  steps,
  currentStep,
  columns,
  fileHandler,
  data,
  width,
  isModelTrainingDone,
  isModelTrainingStarted,
  isDataTransformationDone,
  isDataTransformationStarted
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
    okButtonProps={{ disabled: !isModelTrainingDone }}
  >
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr' }}>
      <Card title="Recoleccion de datos" style={{ width: 200 }}>
        <div style={{ display: 'flex', justifyContent: 'center' }}>
          <Progress type="circle" percent={100} width={80} />
        </div>
      </Card>
      <Card title="Transformacion de datos" style={{ width: 200 }}>
        <div style={{ display: 'flex', justifyContent: 'center' }}>
          {isDataTransformationStarted && !isDataTransformationDone && (
            <Spin
              indicator={<Icon type="loading" style={{ fontSize: 80 }} spin />}
            />
          )}
          {isDataTransformationDone && (
            <Progress type="circle" percent={100} width={80} />
          )}
          {!isDataTransformationStarted && !isDataTransformationDone && (
            <Spin
              indicator={<Icon type="clock-circle" style={{ fontSize: 80 }} />}
            />
          )}
        </div>
      </Card>
      <Card
        title="Entrenamiento del modelo de prediccion"
        style={{ width: 200 }}
      >
        <div style={{ display: 'flex', justifyContent: 'center' }}>
          {isModelTrainingStarted && !isModelTrainingDone && (
            <Spin
              indicator={<Icon type="loading" style={{ fontSize: 80 }} spin />}
            />
          )}
          {isModelTrainingDone && (
            <Progress type="circle" percent={100} width={80} />
          )}
          {!isModelTrainingStarted && !isModelTrainingDone && (
            <Spin
              indicator={<Icon type="clock-circle" style={{ fontSize: 80 }} />}
            />
          )}
        </div>
      </Card>
    </div>
  </Modal>
);
