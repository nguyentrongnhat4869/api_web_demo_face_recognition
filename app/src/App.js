import React, { Component } from "react";
import "./App.css";
import axios from "axios";

class App extends Component {
  state = {
    imgBase64: null,
    file: null,
    response: null
  };

  fileSelectedHandler = event => {
    console.log(event)
    let reader = new FileReader();
    reader.readAsDataURL(event.target.files[0]);
    console.log('event target'+event.target)
    console.log('event file'+event.target.files[0])
    let x = URL.createObjectURL(event.target.files[0]);
    reader.onload = () => {
      this.setState({
        imgBase64: reader.result.split(",")[1],
        file: x,
        response: null
      });
      // console.log(reader.result);
      console.log(x)
      console.log(reader)
    };
  };

  fileUploadHandler = () => {
    const fd = new FormData();
    var imagedata = document.querySelector('input[type="file"]').files[0];
    fd.append("File", imagedata);
    // go ifconfig trong terminal xem ip may minh, thay vao 10.1.70.181
    axios.post("http://10.1.70.181:8000/api/checkimage", fd).then(res => {
      this.setState({
        file: res["data"]["Image"],
        response: "Name: " + res["data"]["DATA"]
      });
      console.log("image"+ JSON.stringify(res["data"]["Image"]))
      console.log("respone"+JSON.stringify(res["data"]["DATA"]))
    });
  };

  getFiles(files) {
    this.setState({
      selectedFile: files
    });
    console.log(files.base64);
  }

  render() {
    return (
      <div className="App">
        <input type="file" onChange={this.fileSelectedHandler} />
        <button onClick={this.fileUploadHandler}>Search </button>
        {this.state.file != null && (
          <div>
            <img src={this.state.file} alt="dcm" width="420" />
          </div>
        )}
        {this.state.response != null && <h1>{this.state.response}</h1>}
        {this.state.response == "" && <h1>Unknown</h1>}
      </div>
    );
  }
}

export default App;
