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

const FormItem = Form.Item;
const Option = Select.Option;
const SHOW_PARENT = TreeSelect.SHOW_PARENT;

// set up period
const Start_year = 1990;
const End_year = 2017;
const children = [];
for (let i = Start_year; i <= End_year; i++) {
    children.push(<Option key={i.toString()}>{i.toString()}</Option>);
}


// set up variable
const variable_children = [];
const all_variables = ['人均国内生产总值','年末总人口','人均可支配收入'];
for (let v in all_variables) {
    variable_children.push(<Option key={all_variables[v]}>{all_variables[v]}</Option>);
}

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            'initperiod': [],
            'period': [],
            'variable':[],
            'region':[],
            'start_year': '',
            'end_year':'',
            'regionselected':[],
            'variableselected':[],
            'table_columns':[],
            'table_data':[],
            'scroll_width': 500,
            'download_file':'',
        };

        this.handleStartYearChange = this.handleStartYearChange.bind(this);
        this.handleEndYearChange = this.handleEndYearChange.bind(this);
        this.handleRegionChange = this.handleRegionChange.bind(this);
        this.handleVariableChange = this.handleVariableChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleTableChange = this.handleTableChange.bind(this);
    }

    init () {
        // 测试时用的网页是 'http://localhost/api?info=database'
        const url = '/api?info=ceicQuery';
        fetch(url)
            .then((resp) => resp.json())
            .then((mydata) =>{
                console.log(mydata.data);

                const children = [];
                for (let i = mydata.data.startYear; i <= mydata.data.endYear; i++) {
                    children.push(<Option key={i.toString()}>{i.toString()}</Option>);
                }
                this.setState({initperiod: children});

                const variable_children = [];
                const all_variables = mydata.data.variable;
                for (let v in all_variables) {
                    variable_children.push(<Option key={all_variables[v]}>{all_variables[v]}</Option>);
                }
                this.setState({variable: variable_children});

                const treeData  = [{
                    label: '所有地区',
                    value: '000000',
                    key: '000000',
                    children: mydata.data.region,
                }];
                this.setState({region: treeData});
            });
    }

    handleStartYearChange(value) {
        const new_period = [];
        for (let i = parseInt(value); i <= End_year; i++) {
            new_period.push(<Option key={i.toString()}>{i.toString()}</Option>);
        }
        this.setState({start_year: value, period: new_period});
    }

    handleEndYearChange(value) {
        this.setState({end_year: value});
    }

    handleRegionChange(value) {
        console.log('onChange ', value, arguments);
        this.setState({
            regionselected: value,
        });
    }

    handleVariableChange(value) {
        console.log('onChange ', value);
        this.setState({
            variableselected: value,
        });
    }

    handleTableChange(pagination) {
        console.log('params', pagination);
    }

    handleSubmit(e) {
        e.preventDefault();
        console.log(this.state.start_year,this.state.end_year,this.state.regionselected,this.state.variableselected);

        const url = '/query';
        fetch(url,{
            method: "POST",
            body: JSON.stringify({'type':'ceic',
                'variable': this.state.variableselected,
                'region': this.state.regionselected,
                'start_year': this.state.start_year,
                'end_year': this.state.end_year}),
            headers: {
                "Content-Type": "application/json"
            }
        }).then((resp) => resp.json())
            .then((mydata) =>{
                console.log(mydata.data.table_columns, mydata.data.table_data, mydata.data.saved_file)

                this.setState({table_columns: mydata.data.table_columns});
                this.setState({table_data: mydata.data.table_data});
                this.setState({scroll_width: mydata.data.width})

                this.setState({download_file: mydata.data.saved_file})
            })
    };

    componentDidMount() {
        this.init();
    }

    render(){
        const tProps = {
            treeData: this.state.region,
            onChange: this.handleRegionChange,
            allowClear: true,
            treeCheckable: true,
            showCheckedStrategy: SHOW_PARENT,
            searchPlaceholder: '选择地区',
            style: {
                width: 200,
            },
        };
        return (
            <div>
                <h4 id="what-is-prometheus?">数据查询</h4>
                <br/>
                <Form layout="inline" onSubmit={this.handleSubmit}>
                    <FormItem>
                        <Select style={{ width: 100 }} placeholder="起始年份" onChange={this.handleStartYearChange}>
                            {this.state.initperiod}
                        </Select>
                    </FormItem>
                    <FormItem>
                        <Select style={{ width: 100 }} placeholder="结束年份" onChange={this.handleEndYearChange}>
                            {this.state.period}
                        </Select>
                    </FormItem>
                    <FormItem>
                        <TreeSelect {...tProps} />
                    </FormItem>
                    <FormItem>
                        <Select mode="multiple" allowClear={true} style={{ width: 200 }} placeholder="选择变量" onChange={this.handleVariableChange}>
                            {this.state.variable}
                        </Select>
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
                    <Col span={6} offset={6}><Button href={this.state.download_file}>数据下载</Button></Col>
                </Row>
                <br/>
                <Table columns={this.state.table_columns} dataSource={this.state.table_data} scroll={{  x: this.state.scroll_width }} onChange={this.handleTableChange} />
            </div>
        );
    }
}

ReactDOM.render(
    <App />,
    document.getElementById('root')
);