import React from 'react';

class PlayerProfile extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    const { currentUser } = this.props;

    console.log(currentUser);

    return (
      <div>
        Your player profile!
      </div>
    )
  }
}

export default PlayerProfile;
