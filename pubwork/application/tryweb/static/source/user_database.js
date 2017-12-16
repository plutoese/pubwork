import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import Table from 'antd/lib/table';  // 加载 JS
import Icon from 'antd/lib/icon';  // 加载 JS

const columns = [{
    title: '数据库',
    dataIndex: 'database_name',
    key: 'database_name',
    render: (text, record) => <a href={record.database_link}>{text}</a>,
}, {
    title: '简介',
    dataIndex: 'database_intro',
    key: 'database_intro',
}, {
    title: '类型',
    dataIndex: 'database_type',
    key: 'database_type',
}];

class App extends Component {
    constructor(props) {
        super(props);
        this.state = { data: [] };
    }

    componentDidMount() {
        // 测试时用的网页是 'http://localhost/api?info=database'
        const url = '/api?info=database';
        fetch(url)
            .then((resp) => resp.json())
            .then((mydata) =>{
                console.log(mydata.data);
                console.log('Hello World');
                this.setState({data: mydata.data});
            });
    }

    render (){
        return (
            <Table dataSource={this.state.data} columns={columns} />
        );
    }
}

ReactDOM.render(
    <App />,
    document.getElementById('root')
);