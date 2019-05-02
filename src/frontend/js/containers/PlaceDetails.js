import React, { Component } from "react";
import "./PlaceDetails.css";
import EventCard from "./EventCard";
import ArtistCard from "./ArtistCard";
import {Container, Row, Col, Card, CardImg, CardText, CardBody, CardTitle, CardSubtitle, Button} from "reactstrap";

class PlaceDetails extends Component {
	constructor() {
		super();
		this.state = {
			events: [
				{
					id: 1,
					eventStatus: "Past Event",
					eventTitle: "Old Event",
					eventDate: "04/01/2019",
					eventDetails: "Prior Event"
				},
				{
					id: 2,
					eventStatus: "Past Event",
					eventTitle: "Old Event",
					eventDate: "04/01/2019",
					eventDetails: "Prior Event"
				},
				{
					id: 3,
					eventState: "Past Event",
					eventTitle: "Old Event",
					eventDate: "04/01/2019",
					eventDetails: "Prior Event"
				}
			],
			place: [
				{
					id: 1,
					hostName: "Host",
					location: "Cambridge, MA",
					description: "Lorem Ipsum",
					seeking: "abstract painting, b&w  photography"
				}
			]

		}
	}

	render() {
		let HistoryCards = this.state.events.map(event => {
			return(
				<Col sm="4">
					<HistoryCards key={event.id} event={event} />
				</Col>
				)
		});

		let PlaceCard = this.state.place.map(place => {
			return(
				<Col sm="4">
					<PlaceCard key={place.id} place={place} />
				</Col>
			)
		});

		return (
			<Container fluid>
				<Row>
					<Col-lg>
						// Place pictures
					</Col-lg>
					<Col-lg>
						// Place map
					</Col-lg>
				</Row>
				<Row>
					{ArtistCard}
				</Row>
				<Row>
					{HistoryCards}
				</Row>
			</Container>
			);
	}
}

export default PlaceDetails;