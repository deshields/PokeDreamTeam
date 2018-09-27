import React, { Component } from 'react';
import PokeAuto from 'pokeform';
import MoveAuto from 'moveform';


class TodoApp extends React.Component {
  constructor(props) {
    super(props);
    this.state = { items: [], text: '' };
    // write props.id or something on input
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  render() {
    return (
      <div>
        <h3>TODO</h3>
        <TodoList items={this.state.items} /> //holds the pokemon
        <form onSubmit={this.handleSubmit}>
          <label htmlFor="new-todo">
            Pokemon #{this.state.items.length+1}
          </label>
          // <input
          //   id={this.state.items.length}
          //   onChange={this.handleChange}
          //   value={this.state.text}
          // />
          <PokeAuto id={this.state.items.length} />
          <button>
            Add #{this.state.items.length + 1}
          </button>
        </form>
      </div>
    );
  }

  handleChange(e) {
    this.setState({ text: e.target.value });
  }

  handleSubmit(e) {
    e.preventDefault();
    if (!this.state.text.length || this.state.text.length == 6) {
      return;
    }
    const newItem = {
      text: this.state.text,
      id: Date.now()
    };
    this.setState(state => ({
      items: state.items.concat(newItem),
      text: ''
    }));
  }
}

class TodoList extends React.Component {
  render() {
    return (
      <ul>
        {this.props.items.map(item => (
          <li key={item.id}>{item.text}</li>
        ))}
      </ul>
    );
  }
}
