import React, { Component } from "react";
import { Button, FormGroup, FormControl, ControlLabel } from "react-bootstrap";
import "./Signup.css";

export default class Signup extends Component {
	constructor(props) {
		super(props);

		this.state = {
			first_name: "",
			last_name: "",
			email: "",
			password: "",
			confirm_password: ""
		};
		this.handleChange = this.handleChange.bind(this);
		this.handleSubmit = this.handleSubmit.bind(this);
	}

	validateForm() {
		return this.state.first_name.length > 0 && this.state.last_name > 0 && this.state.email > 0 && this.state.password > 0 & this.state.password == this.state.confirm_password; // Maybe add some more restrictions here like ensuring these inputs aren't too long or that the passwords have some minimum complexity
	}

	handleChange(event) {
		this.setState({
			[event.target.id]: event.target.value
		});
	}

	handleSubmit(event) {
		event.preventDefault();

        fetch('/api/auth', {
            method: 'POST',
                body: JSON.stringify({first_name: this.state.first_name, last_name: this.state.last_name, email: this.state.email, password: this.state.password}),
            })
                    .then(function(res) {
                        return res.json();
                    })
                    .then(function(result) {
                        alert(JSON.stringify(result))
                    });
	}

	render() {
		return (
			 <div className="Signup">
                <form onSubmit={this.handleSubmit}>
                	 <FormGroup controlId="first_name" bsSize="large">
                	 	<ControlLabel>First Name</ControlLabel>
                	 	<FormControl
                	 		autoFocus
                	 		name="first_name"
                	 		type="text"
                	 		value={this.state.first_name}
                	 		onChange={this.handleChange}
                	 	/>
                	 </FormGroup>
                	 <FormGroup controlId="last_name" bsSize="large">
                	 	<ControlLabel>Last Name</ControlLabel>
                	 	<FormControl
                	 		autoFocus
                	 		name="last_name"
                	 		type="text"
                	 		value={this.state.last_name}
                	 		onChange={this.handleChange}
                	 	/>
                	 </FormGroup>
                     <FormGroup controlId="email" bsSize="large">
                        <ControlLabel>Email</ControlLabel>
                        <FormControl
                            autoFocus
														name="email"
                            type="email"
                            value={this.state.email}
                            onChange={this.handleChange}
                        />
                    </FormGroup>
                    <FormGroup controlId="password" bsSize="large">
                        <ControlLabel>Password</ControlLabel>
                        <FormControl
                            value={this.state.password}
                            onChange={this.handleChange}
                            name="password"
														type="password"
                        />
                    </FormGroup>
                    <FormGroup controlId="confirm_password" bsSize="large">
                        <ControlLabel>Retype Password</ControlLabel>
                        <FormControl
                            value={this.state.confirm_password}
                            onChange={this.handleChange}
                            name="confirm_password"
														type="password"
                        />
                    </FormGroup>
                    <Button
                        block
                        bsSize="large"
                        disabled={!this.validateForm()}
                        type="submit"
                    >
                        Sign Up
                    </Button>
                </form>
            </div>
			);
	}

}