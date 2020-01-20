import React, { Component } from 'react';

class Playerform extends React.Component {
  constructor(props) {
    super(props);
    this.state = { items: [], text: '' };
    this.delete = this.delete.bind(this)

  }

  delete(id){
   this.setState(prevState => ({
       items: prevState.items.filter(el => el != id )
   })
  );
 }

  render() {
    return (
      <div className="TeamSide">
        <h3>{this.props.side} Team </h3>

        <TeamList items={this.state.items} delete={this.delete}/>

      </div>
    );
  }

}

class TeamList extends React.Component {
  delete(id){
    this.props.delete(id);
  }

  render() {
    return (
      <div className="Teamlist">
        <ul>
          {this.props.items.map(item => (
            <li key={this.props.items.indexOf(item)}><input type="image" src={item.all.sprite} className={'spriteImg'} onClick={this.delete.bind(this,item)}/></li>
          ))}
        </ul>
      </div>
    );
  }
}

export default Playerform;
