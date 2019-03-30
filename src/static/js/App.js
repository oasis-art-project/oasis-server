import React, { Component } from "react";
import { Link } from "react-router-dom";
import { Nav, Navbar, NavItem } from "react-bootstrap";
import "./App.css";
import Routes from "./Routes";
import { LinkContainer } from "react-router-bootstrap";
import {Button} from "react-bootstrap";
import {Col, Row} from "reactstrap";

const footerStyle = {
  backgroundColor: "#C5DDDB",
  fontSize: "20px",
  color: "white",
  borderTop: "1px solid #E7E7E7",
  textAlign: "center",
  padding: "20px",
  position: "fixed",
  left: "0",
  bottom: "0",
  height: "60px",
  width: "100%"
};

const phantomStyle = {
  display: "block",
  padding: "25px",
  height: "60px",
  width: "100%"
};

function Footer({ children }) {
  return (
      <div>
        <div style={phantomStyle} />
        <div style={footerStyle}>{children}</div>
      </div>
  );
}


class App extends Component {
  render() {
    return (
        <div className="App container">
          <Navbar fluid collapseOnSelect>
            <Navbar.Header>
              <Navbar.Brand>
                <Link to="/"><img src={require('./containers/assets/oasis_logo.png')} weight="40" height="40" alt="OasisLogo"/></Link>
              </Navbar.Brand>
              <Navbar.Toggle />
            </Navbar.Header>
            <Navbar.Collapse>
              <Nav pullRight>
                <LinkContainer to="/containers/EventPage">
                  <NavItem><Button href="./containers/EventPage.js">Event Page</Button></NavItem>
                </LinkContainer>
                <LinkContainer to="/signup">
                  <NavItem><Button href="/signup">Sign Up</Button></NavItem>
                </LinkContainer>
                <LinkContainer to="/login">
                  <NavItem><Button href="/login">Login</Button></NavItem>
                </LinkContainer>
              </Nav>
            </Navbar.Collapse>
          </Navbar>
          <Routes />
          <Footer>
            <p>&copy; OASIS 2019</p>
          </Footer>

        </div>



    );
  }
}

export default App;