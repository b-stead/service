import React, { Component } from "react";
import {
  Button,
  Modal,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Form,
  FormGroup,
  Input,
  Label,
} from "reactstrap";

export default class CustomModal extends Component {
  constructor(props) {
    super(props);
    this.state = {
      activeItem: this.props.activeItem,
    };
  }

  handleChange = (e) => {
    let { name, value } = e.target;

    if (e.target.type === "checkbox") {
      value = e.target.checked;
    }

    const activeItem = { ...this.state.activeItem, [name]: value };

    this.setState({ activeItem });
  };

  render() {
    const { toggle, onSave } = this.props;

    return (
      <Modal isOpen={true} toggle={toggle}>
        <ModalHeader toggle={toggle}>User</ModalHeader>
        <ModalBody>
          <Form>
            <FormGroup>
              <Label for="todo-title">Email</Label>
              <Input
                type="email"
                id="user-email"
                name="email"
                value={this.state.activeItem.email}
                onChange={this.handleChange}
                placeholder="User Email"
              />
            </FormGroup>
            <FormGroup>
              <Label for="todo-description">First Name</Label>
              <Input
                type="text"
                id="user-first-name"
                name="first-name"
                value={this.state.activeItem.first_name}
                onChange={this.handleChange}
                placeholder="Enter User first Name"
              />
            </FormGroup>
            <FormGroup check>
              <Label check>
                <Input
                  type="checkbox"
                  name="completed"
                  checked={this.state.activeItem.completed}
                  onChange={this.handleChange}
                />
                Completed
              </Label>
            </FormGroup>
          </Form>
        </ModalBody>
        <ModalFooter>
          <Button
            color="success"
            onClick={() => onSave(this.state.activeItem)}
          >
            Save
          </Button>
        </ModalFooter>
      </Modal>
    );
  }
}