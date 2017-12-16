/*
@title: 城市统计数据库查询UI
@author: Glen
@date: 2017.12.11
@intro: 城市统计数据库的查询界面，其中包括数据查询，结果显示以及数据保存等功能
@tag: city database
 */

import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import Row from 'antd/lib/row';  // 加载 JS
import Col from 'antd/lib/col';
import Button from 'antd/lib/button';  // 加载 JS
import Form from 'antd/lib/form';  // 加载 JS
import Select from 'antd/lib/select';
import TreeSelect from 'antd/lib/tree-select';
import Divider from 'antd/lib/divider';
import Table from 'antd/lib/table';
import Radio from 'antd/lib/radio';
import Input from 'antd/lib/input';

/*
初始化必要的常量
 */
const FormItem = Form.Item;
const Option = Select.Option;
const SHOW_ALL = TreeSelect.SHOW_ALL;
const RadioGroup = Radio.Group;
const user = document.getElementById('username').getAttribute('value');

/*
核心类App
 */
class App extends Component {
    constructor(props) {
        super(props);
        // 设置状态
        this.state = {
            // 初始时间选择跨度变量，用于起始时间选择框
            'initPeriod': [],
            // 时间跨度变量，用于终止时间选择框
            'period': [],
            // 指标变量，用于变量选择框
            'variable':[],
            // 地区变量，用于地区树形选择框
            'region':[],
            // 数据查询的起始年份，用于提交到服务器，初始化时设置为数据库起始时间
            'startYear': '',
            // 数据查询的终止年份，用于提交到服务器，初始化时设置为数据库的结束时间
            'endYear':'',
            // 数据查询选择的地区，用于提交到服务器
            'regionSelected':[],
            // 数据查询选择的变量，用于提交到服务器
            'variableSelected':[],
            // 数据表格的列变量，从服务器获得数据
            'tableColumns':[],
            // 数据表格的数据，从服务器获得数据
            'tableData':[],
            // 数据表格的宽度，随着变量数量的变化而变化，初始值为500， 之后从服务器获得数据
            'scrollWidth': 500,
            //  数据表格的下载链接文件，用于数据下载按钮
            'downloadFile':'',
            // 数据查询的区域范围变量，全市用1，市辖区用2
            'scale': 1,
            // 数据保存按钮后的信息显示变量，显示已保存，超出限制数量等
            'datasetSavingMessage':'',
            // 待保存的数据集名称变量，用于提交到服务器
            'datasetName':'',
        };

        this.handleStartYearChange = this.handleStartYearChange.bind(this);
        this.handleEndYearChange = this.handleEndYearChange.bind(this);
        this.handleRegionChange = this.handleRegionChange.bind(this);
        this.handleVariableChange = this.handleVariableChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleTableChange = this.handleTableChange.bind(this);
        this.handleScaleChange = this.handleScaleChange.bind(this);
        this.handleDatasetName = this.handleDatasetName.bind(this);
        this.handleSaveDataset = this.handleSaveDataset.bind(this);
    }

    /*
    初始化网页，其中包括以下几个方面：
    1. 从服务器的查询接口获得(fetch)构建界面所需的数据
    2. 设置状态变量：（1）起始时间选择框；（2）变量选择框；（3）地区树形选择框
     */
    init () {
        // 测试时用的网页是 'http://localhost/api?info=database'
        console.log('init',user);
        const url = '/api?info=citystatquery';
        fetch(url)
            .then((resp) => resp.json())
            .then((mydata) =>{
                // 用于测试时显示服务器获得的数据
                console.log(mydata.data);

                // 起始时间选择框children
                const startYearChildren = [];
                for (let i = mydata.data.startYear; i <= mydata.data.endYear; i++) {
                    startYearChildren.push(<Option key={i.toString()}>{i.toString()}</Option>);
                }
                this.setState({
                    startYear: mydata.data.startYear,
                    endYear: mydata.data.endYear,
                    initPeriod: startYearChildren
                });

                // 变量选择框variableChildren
                const variableChildren = [];
                const all_variables = mydata.data.variable;
                for (let v in all_variables) {
                    variableChildren.push(<Option key={all_variables[v]}>{all_variables[v]}</Option>);
                }
                this.setState({variable: variableChildren});

                // 地区选择框regionSelectData
                const regionSelectData  = [{
                    label: '所有地区',
                    value: '000000',
                    key: '000000',
                    children: mydata.data.region,
                }];
                this.setState({region: regionSelectData});
            });
    }

    /*
    处理起始时间框变化（选择）的事件：（1）保存选择的起始时间到startYear；（2）对结束时间选择框用newPeriod进行赋值
     */
    handleStartYearChange(value) {
        const newPeriod = [];
        for (let i = parseInt(value); i <= this.state.endYear; i++) {
            newPeriod.push(<Option key={i.toString()}>{i.toString()}</Option>);
        }
        this.setState({startYear: value, period: newPeriod});
    }

    /*
    处理结束时间框变化（选择）的事件：保存选择的结束时间到endYear
     */
    handleEndYearChange(value) {
        this.setState({endYear: value});
    }

    /*
    处理地区选择框变化（选择）的事件：保存选择的地区到regionSelected
     */
    handleRegionChange(value) {
        // 测试时使用
        //console.log('onChange ', value, arguments);
        this.setState({
            regionSelected: value,
        });
    }

    /*
     处理变量选择框变化（选择）的事件：保存选择的变量到variableSelected
     */
    handleVariableChange(value) {
        // 测试时使用
        //console.log('onChange ', value);
        this.setState({
            variableSelected: value,
        });
    }

    /*
     处理变量名输入框变化（选择）的事件：（1）清除数据集保存反馈信息datasetSavingMessage；（2）保存输入的数据集名称到datasetName
     */
    handleDatasetName(e) {
        // 测试时使用
        // console.log('oninputChange ', e.target.value);
        this.setState({
            datasetSavingMessage: "",
            datasetName: e.target.value,
        });
    }

    /*
     处理数据表格框变化（选择）的事件：无对应处理方法
     */
    handleTableChange(pagination) {
        console.log('params', pagination);
    }

    /*
     处理地区范围选择框变化（选择）的事件：保存选择的变量到scale
     */
    handleScaleChange(e) {
        console.log('onChange ', e.target.value);
        this.setState({
            scale: e.target.value,
        });
    }

    /*
     处理数据查询提交的事件：（1）验证数据查询框是否选择（或填写）；
                             （2）如果验证成功，向服务器提交查询(fetch)；
                             （3）获得服务器返回的数据，对变量进行赋值
     */
    handleSubmit(e) {
        e.preventDefault();
        this.props.form.validateFields(['startYear','endYear','region','variable'],(err, values) => {
            if (!err) {
                // 测试时使用
                console.log(this.state.startYear,this.state.endYear,this.state.regionSelected,this.state.variableSelected,this.state.scale);

                const url = '/query';
                fetch(url,{
                    method: "POST",
                    body: JSON.stringify({'type':'citystat',
                        'variable': this.state.variableSelected,
                        'region': this.state.regionSelected,
                        'start_year': this.state.startYear,
                        'end_year': this.state.endYear,
                        'boundary': this.state.scale,
                    }),
                    headers: {
                        "Content-Type": "application/json"
                    }
                }).then((resp) => resp.json())
                    .then((mydata) =>{
                        // 测试时使用
                        console.log(mydata.data.tableColumns, mydata.data.tableData, mydata.data.saved_file);

                        // 对数据表格进行赋值
                        this.setState({tableColumns: mydata.data.table_columns});
                        this.setState({tableData: mydata.data.table_data});
                        this.setState({scrollWidth: mydata.data.width});

                        // 把下载链接赋值到this.state.downloadFile
                        this.setState({downloadFile: mydata.data.saved_file})
                    });
                this.setState({datasetSavingMessage: ''})
            }
        });

    };

    /*
     处理数据集保存提交的事件：（1）验证数据集名称是否填写；
                               （2）如果验证成功，查看当前是否有数据查询结果，如果没有，返回信息“无数据保存”；
                               （3）如果验证成果且有数据表格，则提交信息到服务器，保存数据集
                               （4）接收服务器返回信息，并显示
     */
    handleSaveDataset(e) {
        e.preventDefault();
        this.props.form.validateFields(['datasetName'],(err, values) => {
            if (!err) {
                // 测试时使用
                console.log('nextonChange ', this.state.datasetName,user);

                if (this.state.downloadFile == '') {
                    this.setState({datasetSavingMessage: '无数据保存'});
                } else{
                    const url = '/savedataset';
                    fetch(url,{
                        method: "POST",
                        body: JSON.stringify({
                            'user':user,
                            'savedDatasetName':this.state.downloadFile,
                            'newDatasetName': this.state.datasetName,
                        }),
                        headers: {
                            "Content-Type": "application/json"
                        }
                    }).then((resp) => resp.json())
                        .then((mydata) =>{
                            console.log(mydata.data);
                            this.setState({datasetSavingMessage: mydata.data.message});
                        })
                }
            }
        });
    }

    componentDidMount() {
        this.init();
    }

    render(){
        const { getFieldDecorator } = this.props.form;
        const tProps = {
            treeData: this.state.region,
            onChange: this.handleRegionChange,
            allowClear: true,
            treeCheckable: true,
            showCheckedStrategy: SHOW_ALL,
            searchPlaceholder: '选择地区',
            style: {
                width: 180,
            },
        };
        const radioStyle = {
            display: 'block',
            height: '20px',
            lineHeight: '20px',
        };

        return (
            <div>
                <h4 id="what-is-prometheus?">数据查询</h4>
                <br/>
                <Form layout="inline" onSubmit={this.handleSubmit}>
                    <FormItem>
                        {getFieldDecorator('startYear', {
                            rules: [{ required: true, message: '请选择起始年份!' }],
                        })(
                            <Select style={{ width: 90 }} placeholder="起始年份" onChange={this.handleStartYearChange}>
                                {this.state.initPeriod}
                            </Select>
                        )}
                    </FormItem>
                    <FormItem>
                        {getFieldDecorator('endYear', {
                            rules: [{ required: true, message: '请选择结束年份!' }],
                        })(
                            <Select style={{ width: 90 }} placeholder="结束年份" onChange={this.handleEndYearChange}>
                                {this.state.period}
                            </Select>
                        )}
                    </FormItem>
                    <FormItem>
                        {getFieldDecorator('region', {
                            rules: [{ required: true, message: '请选择地区!' }],
                        })(
                            <TreeSelect {...tProps} />
                        )}
                    </FormItem>
                    <FormItem>
                        {getFieldDecorator('variable', {
                            rules: [{ required: true, message: '请选择变量!' }],
                        })(
                            <Select mode="multiple" allowClear={true} style={{ width: 180 }} dropdownMatchSelectWidth={false}
                                    placeholder="选择变量" onChange={this.handleVariableChange}>
                                {this.state.variable}
                            </Select>
                        )}
                    </FormItem>
                    <FormItem>
                        <RadioGroup onChange={this.handleScaleChange} value={this.state.scale}>
                            <Radio style={radioStyle} value={1}>全市</Radio>
                            <Radio style={radioStyle} value={2}>市辖区</Radio>
                        </RadioGroup>
                    </FormItem>
                    <FormItem>
                        <Button type="primary" htmlType="submit">
                            确定
                        </Button>
                    </FormItem>
                </Form>
                <Divider/>
                <Row>
                    <Col span={8}><h4 id="what-is-prometheus?">查询结果</h4></Col>
                    <Col span={16}>
                        <Form layout="inline" onSubmit={this.handleSaveDataset}>
                            <FormItem>
                                <Button href={this.state.downloadFile}>数据下载</Button>
                            </FormItem>
                            <FormItem>
                                {getFieldDecorator('datasetName', {
                                    rules: [{ required: true, message: '请输入数据集名称!' }],
                                })(
                                    <Input style={{ width: 240 }} addonAfter={this.state.datasetSavingMessage}
                                           placeholder="请输入数据集名称" onChange={this.handleDatasetName} />
                                )}
                            </FormItem>
                            <FormItem>
                                <Button htmlType="submit">保存数据集</Button>
                            </FormItem>
                        </Form>
                    </Col>
                </Row>
                <br/>
                <Table columns={this.state.tableColumns} dataSource={this.state.tableData}
                       scroll={{ x: this.state.scrollWidth }} onChange={this.handleTableChange} />
            </div>
        );
    }
}

const WrappedApp = Form.create()(App);

ReactDOM.render(
    <WrappedApp />,
    document.getElementById('root')
);