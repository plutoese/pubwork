/*
 @title: 我的数据集管理
 @author: Glen
 @date: 2017.12.14
 @intro: 管理我的数据集，其中包括修改标注，简介等
 @tag: dataset
 */

import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import Table from 'antd/lib/table';
import Button from 'antd/lib/button';
import Input from 'antd/lib/input';
import Popconfirm from 'antd/lib/popconfirm';
import Icon from 'antd/lib/icon';
import Divider from 'antd/lib/divider';
import Upload from 'antd/lib/upload';
import message from 'antd/lib/message';

const user = document.getElementById('username').getAttribute('value');

/*
 可修改的单元格类
 */
class EditableCell extends React.Component {
    /*
     初始化
     */
    constructor(props) {
        super(props);
        this.state =  {
            value: this.props.value,
            // 初始化是editable是false
            editable: false,
        };

        this.handleChange = this.handleChange.bind(this);
        this.check = this.check.bind(this);
        this.edit = this.edit.bind(this);
    }

    /*
     处理单元格的值发生变化的事件：重设value
     */
    handleChange(e) {
        const value = e.target.value;
        this.setState({ value });
    }

    /*
     处理修改完毕回车或者点击完成的事件：重设this.state.editable为false，调用this.props.onChange函数来进行处理
     */
    check (){
        this.setState({ editable: false });
        if (this.props.onChange) {
            this.props.onChange(this.state.value);
        }
    }

    /*
     处理点击编辑图标的事件：把this.state.editable的状态设为true
     */
    edit(){
        this.setState({ editable: true });
    }

    render() {
        const { value, editable } = this.state;
        return (
            <div className="editable-cell">
                {
                    /*
                     是否编辑状态，这里有个选择，如果是，显示Input和Icon；否则显示值和Icon。
                     */
                    editable ?
                        <div className="editable-cell-input-wrapper">
                            <Input value={value} onChange={this.handleChange} onPressEnter={this.check} />
                            <Icon type="check" className="editable-cell-icon-check" onClick={this.check} />
                        </div>
                        :
                        <div className="editable-cell-text-wrapper">
                            {value || ' '}
                            <Icon type="edit" className="editable-cell-icon" onClick={this.edit} />
                        </div>
                }
            </div>
        );
    }
}

/*
 可编辑的表格
 */
class EditableTable extends React.Component {
    /*
     初始化表格
     */
    constructor(props) {
        super(props);

        this.state = {
            dataSource: [],
            update_return : '',
            file_link: {},
            dataset_status: undefined,
            fileList: [],
        };

        this.columns = [{
            title: '名称',
            dataIndex: 'name',
            width: '20%',
        }, {
            title: '标识',
            dataIndex: 'label',
            width: '20%',
            render: (text, record) => (
                <EditableCell value={text} onChange={this.onCellChange(record.key, 'label')} />
            ),
        }, {
            title: '简介',
            dataIndex: 'introduction',
            width: '35%',
            render: (text, record) => (
                <EditableCell value={text} onChange={this.onCellChange(record.key, 'introduction')} />
            ),
        },{
            title: '操作',
            dataIndex: 'operation',
            render: (text, record) => {
                const {dataset_status} = this.state;
                const status = dataset_status[record.name];
                console.log('herecomes',dataset_status,record.name,dataset_status[record.name],status);
                return (
                    <span>
                        <a href={this.state.file_link[record.name]}>下载</a>
                        <Divider type="vertical" />
                        {status ?
                            <Popconfirm title="确定设为私密?" onConfirm={() => this.onPrivate(record.key)}>
                                <a href="#">设为私密</a>
                            </Popconfirm>
                            :
                            <Popconfirm title="确定设为公开?" onConfirm={() => this.onPublic(record.key)}>
                                <a href="#">设为公开</a>
                            </Popconfirm>}
                        <Divider type="vertical" />
                        <Popconfirm title="确定删除?" onConfirm={() => this.onDelete(record.key)}>
                            <a href="#">删除</a>
                        </Popconfirm>
                    </span>
                );
            },
        }];

        this.onCellChange = this.onCellChange.bind(this);
        this.onDelete = this.onDelete.bind(this);
        this.onPrivate = this.onPrivate.bind(this);
        this.onPublic = this.onPublic.bind(this);
        this.uploadFile = this.uploadFile.bind(this);
    }

    init() {
        // 测试时用的网页是 'http://localhost/api?info=database'
        const url = `http://localhost/datasetmanger?info=mydataset&user=${user}`;
        fetch(url)
            .then((resp) => resp.json())
            .then((mydata) =>{
                console.log(mydata.data);
                this.setState({
                    dataSource: mydata.data.table_data,
                    file_link: mydata.data.file_link,
                    dataset_status: mydata.data.dataset_status,
                });
            });
    }

    update_value(name,dataIndex,value){
        const url = 'http://localhost/datasetmanger';
        fetch(url,{
            method: "POST",
            body: JSON.stringify({
                'type':'update',
                'user': `${user}`,
                'datasetName': name,
                'dataIndex': dataIndex,
                'value': value}),
            headers: {
                "Content-Type": "application/json"
            }
        }).then((resp) => resp.json())
            .then((mydata) =>{
                // 测试时使用
                console.log('return',mydata.data.updated);
                this.setState({update_return: mydata.data.updated});
            });
    }

    componentDidMount() {
        this.init()
    }

    /*
     编辑单元格事件
     */
    onCellChange(key, dataIndex) {
        return (value) => {
            const dataSource = [...this.state.dataSource];
            const target = dataSource.find(item => item.key === key);
            if (target) {
                console.log('before: ',target,'->',target['name'],dataIndex,value);
                this.update_value(target['name'],dataIndex,value);
                target[dataIndex] = this.state.update_return;
                this.setState({ dataSource });
                console.log('after: ',target);
            }
        };
    }

    onDelete(key) {
        const dataSource = [...this.state.dataSource];
        const target = dataSource.find(item => item.key === key);

        const url = 'http://localhost/datasetmanger';
        fetch(url,{
            method: "POST",
            body: JSON.stringify({
                'type':'delete',
                'user': `${user}`,
                'datasetName': target['name']
            }),
            headers: {
                "Content-Type": "application/json"
            }
        }).then((resp) => resp.json())
            .then((mydata) =>{
                // 测试时使用
                //console.log('return',mydata.data.deleted);
                if (mydata.data.deleted) {
                    this.setState({ dataSource: dataSource.filter(item => item.key !== key) });
                }
            });
    }

    onPublic(key) {
        const dataSource = [...this.state.dataSource];
        const datasetStatus = this.state.dataset_status;
        const target = dataSource.find(item => item.key === key);

        const url = 'http://localhost/datasetmanger';
        fetch(url,{
            method: "POST",
            body: JSON.stringify({
                'type':'toPublic',
                'user': `${user}`,
                'datasetName': target['name'],
            }),
            headers: {
                "Content-Type": "application/json"
            }
        }).then((resp) => resp.json())
            .then((mydata) =>{
                // 测试时使用
                //console.log('return',mydata.data.deleted);
                datasetStatus[target['name']] = mydata.data.public;
                this.setState({ datasetStatus });
            });
    }

    onPrivate(key) {
        const dataSource = [...this.state.dataSource];
        const datasetStatus = this.state.dataset_status;
        const target = dataSource.find(item => item.key === key);

        const url = 'http://localhost/datasetmanger';
        fetch(url,{
            method: "POST",
            body: JSON.stringify({
                'type':'toPrivate',
                'user': `${user}`,
                'datasetName': target['name'],
            }),
            headers: {
                "Content-Type": "application/json"
            }
        }).then((resp) => resp.json())
            .then((mydata) =>{
                // 测试时使用
                //console.log('return',mydata.data.deleted);
                datasetStatus[target['name']] = mydata.data.public;
                this.setState({ datasetStatus });
            });
    }

    uploadFile (info) {
        let fileList = info.fileList;

        // 1. Limit the number of uploaded files
        //    Only to show two recent uploaded files, and old ones will be replaced by the new
        fileList = fileList.slice(-1);

        // 2. read from response and show file link
        fileList = fileList.map((file) => {
            if (file.response) {
                // Component will show file.url as link
                file.url = file.response.url;
            }
            return file;
        });

        // 3. filter successfully uploaded files according to response from server
        fileList = fileList.filter((file) => {
            if (file.response) {
                return file.response.status === 'success';
            }
            return true;
        });

        this.setState({ fileList });
        this.init();
    }

    render() {
        const { dataSource } = this.state;
        const columns = this.columns;
        const upload_props = {
            action: 'http://localhost/upload',
            onChange: this.uploadFile,
            multiple: false,
            headers: {
                authorization: 'authorization-text',
                user: user,
            },
        };
        return (
            <div>
                <h4 id="what-is-prometheus?">我的数据集</h4>
                <br/>
                <Upload {...upload_props} fileList={this.state.fileList}>
                    <Button>
                        <Icon type="upload" /> 上传我的数据文件
                    </Button>
                </Upload>
                <br />
                <Table bordered dataSource={dataSource} columns={columns} />
            </div>
        );
    }
}

ReactDOM.render(<EditableTable />, document.getElementById('root'));
