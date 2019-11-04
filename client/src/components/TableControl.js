import React from 'react';
import { Table } from 'antd';

export default ({ data, columns }) => (
  <Table
    columns={columns}
    dataSource={data}
    pagination={{ defaultPageSize: 5 }}
  />
);
