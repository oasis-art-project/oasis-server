import React, {Component} from "react";
import {Card, CardBody, CardImg, CardSubtitle, CardText, CardTitle} from "reactstrap";
import {Button} from "reactstrap";
import oasis_logo from './assets/oasis_logo.png';
import CardHeader from "reactstrap/es/CardHeader";
import "./PlaceCard.css";


class PlaceCard extends Component {
	render() {
		let {id, , placeName, hostName, location, description, seeking} = this.props.place;
		return (
			<div>
                <Card className="card-body">
                    <CardHeader>{placename}</CardHeader>
                    <CardImg top width="50%" src={oasis_logo} alt="Card image cap" /> // add place image here
                    <CardBody>
                        <CardTitle>{hostName}</CardTitle>
                        <CardSubtitle>{location}</CardSubtitle>
                        <CardSubtitle>{seeking}</CardSubtitle>
                        <CardText>{description}</CardText>
                        <Button color="primary" size="sm" href="#">Contact</Button>
                    </CardBody>
                </Card>
            </div>
			)
	}
}

export default PlaceCard;