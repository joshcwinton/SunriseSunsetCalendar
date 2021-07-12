import React, { Component } from "react";

class ZipForm extends Component {
  render() {
    return (
      <form onSubmit={console.log("hello")}>
        <label>
          ZIP Code:
          <input type="text" name="zip" />
        </label>
        <input type="submit" value="Submit" />
      </form>
    );
  }
}

export default ZipForm;
