import React, { Component } from 'react';

class Playerform extends React.Component {
  constructor(props) {
    super(props);
    this.state = { items: [], text: '' };

  }

  render() {
    return (
      <div className="TeamSide">
        <h3>{this.props.side} Team </h3>

        <TodoList items={this.state.items} />

      </div>
    );
  }

}

class TodoList extends React.Component {

  render() {
    return (
      <ul>
        {this.props.items.map(item => (
          <li key={this.props.items.indexOf(item)}><img src={item.sprite} className={'spriteImg'} alt=""/></li>
        ))}
      </ul>
    );
  }
}

export default Playerform;
