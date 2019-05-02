import React, { Component } from "react";
import "./ArtistDetails.css";
import EventCard from "./EventCard";
import ArtistCard from "./ArtistCard";
import {Container, Row, Col, Card, CardImg, CardText, CardBody, CardTitle, CardSubtitle, Button} from "reactstrap";

class ArtistDetails extends Component {
	constructor() {
		super();
		this.state = {
			events: [ /*
				{
					id: 1,
					eventStatus: "Current Event",
					eventTitle: "Todays Event",
					eventDate: "04/05/2019",
					eventDetails: "Come check out todays event"
				},
				{
					id: 2,
					eventStatus: "Upcoming Event",
					eventTitle: "Next weeks event",
					eventDate: "04/10/2019",
					eventDetails: "Come check out next weeks event"
				},
				{
					id: 3,
					eventStatus: "Upcoming Event",
					eventTitle: "Next weeks event",
					eventDate: "04/10/2019",
					eventDetails: "Come check out next weeks event"
				},
				{
					id: 4,
					eventStatus: "Upcoming Event",
					eventTitle: "Next weeks event",
					eventDate: "04/10/2019",
					eventDetails: "Come check out next weeks event"
				},
				{
					id: 5,
					eventStatus: "Past Event",
					eventTitle: "Last weeks event",
					eventDate: "04/01/2019",
					eventDetails: "Come check out next weeks event"
				},
				{
					id: 6,
					eventStatus: "Past Event",
					eventTitle: "Last weeks event",
					eventDate: "04/01/2019",
					eventDetails: "Come check out next weeks event"
				},
				{
					id: 7,
					eventStatus: "Past Event",
					eventTitle: "Last weeks event",
					eventDate: "04/01/2019",
					eventDetails: "Come check out next weeks event"
				} */
			],
			artist: [ /*
				{
					id: 1,
					artistName: "John Smith",
					location: "xyz",
					genres: "illustrator, sculptor",
					description: "lorem ipsum"

				} */
			]
		}
	}

	/* componentDidMount() {
		fetch("/api/event")
			.then(response => response.json())
			.then(data => this.setState({events: data.event}));
		fetch("api/event/artist")
			.then(response => response.json())
			.then(data => this.setState({artist: data.artist}));
	} */

	render() {

		const {hits} = this.state;

		let CurrentCard = this.state.events.map(event => {
			return(
				<Col sm="4">
					<CurrentCard key={event.id} event={event} />
				</Col>
				)
		});

		let ArtistCard = this.state.artist.map(artist => {
			return(
				<Col sm="4">
					<ArtistCard key={artist.id} artist={artist} />
				</Col>
				)

		});

		let UpcomingCards = this.state.events.map(event => {
			return(
				<Col sm="4">
					<UpcomingCards key={event.id} event={event} />
				</Col>
				)
		});

		let HistoryCards = this.state.events.map(event => {
			return(
				<Col sm="4">
					<HistoryCards key={event.id} event={event} />
				</Col>
				)
		});
		
		return (
			<Container fluid>
				<Row>
					<Col-sm>
						// Profile picture here
					</Col-sm>
					<Col-sm>
						// Main artist card
						{ArtistCard}
					</Col-sm>
					<Col-sm>
						// Current Event
						{CurrentCard}
					</Col-sm>
				</Row>
				<Row>
					// Upcoming Events
					{UpcomingCards}
				</Row>
				<Row>
					// Event History
					{HistoryCards}
				</Row>
				<Row>
					// Art works
				</Row>
				<Row>
					// Art Works
				</Row>
			</Container>
		);
	}
}

export default ArtistDetails;
