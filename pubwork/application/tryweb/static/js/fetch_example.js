class ExampleComponent extends React.Component {
  constructor(props){
    super(props);
    this.state = { name: '' };
    this._getRandomName = this.getRandomName.bind(this);
  }

  render() {
    const { name } = this.state;
    return(
      <div>
        <h1>{name}</h1>
        <button
          onClick={this._getRandomName}
        >
          PRESS ME!
        </button>
      </div>
    );
  }

  getRandomName() {
    fetch('https://randomuser.me/api/')
      .then(response => response.json())
      .then(data => {
        console.log(data)
        const person = data.results[0];
        this.setState({ name: `${person.name.first} ${person.name.last}` })
      })
  }
}

const App = () => (
  <div>
    <ExampleComponent />
  </div>
);

ReactDOM.render(<App />, document.getElementById("container"));