import React, { useState } from 'react';
import './App.css';
import shoeImage from './shoe.jpg'; // Adjust the path as necessary

const ProductDetail = () => {
  const [aspectSentiments, setAspectSentiments] = useState({});
  const [showPopup, setShowPopup] = useState('');

  const submitReview = () => {
    const review = document.getElementById('full-review').value.trim();
    if (review !== "") {
      fetch('http://127.0.0.1:5000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ review: review })
      })
      .then(response => response.json())
      .then(data => {
        setAspectSentiments(data);
        console.log(data);
      })
      .catch(error => console.error('Error:', error));
    }
  };

  const showPopupHandler = (area) => {
    if (showPopup === area) {
      setShowPopup('');
    } else {
      setShowPopup(area);
    }
  };

  const updatePopupContents = (aspect) => {
    return aspect ? (
      <p>{aspect.review} - Sentiment: <strong>{aspect.sentiment}</strong> 💬</p>
    ) : (
      <p>No review available for this area.</p>
    );
  };

  return (
    <div>
      <header>
        <h1>Welcome to Our Store! 🎉</h1>
        <nav>
          <ul>
            <li>
              <button className="btn-link" onClick={() => alert('👀 View Larger Image clicked!')}>
                View Larger Image
              </button>
            </li>
            <li>
              <button className="btn-link" onClick={() => alert('📤 Share clicked!')}>
                Share
              </button>
            </li>
          </ul>
        </nav>
      </header>

      <div className="image-container">
        <img src={shoeImage} alt="Product" className="product-image" />

        <div className="click-area sole" style={{ position: 'absolute', top: '150px', left: '210px', width: '150px', height: '60px', backgroundColor: 'rgba(255, 0, 0, 0.1)' }} onClick={() => showPopupHandler('sole')}></div>
        <div className="click-area toe" style={{ position: 'absolute', top: '300px', left: '400px', width: '100px', height: '50px', backgroundColor: 'rgba(0, 255, 0, 0.1)' }} onClick={() => showPopupHandler('toe')}></div>
        <div className="click-area quality" style={{ position: 'absolute', top: '260px', left: '420px', width: '70px', height: '50px', backgroundColor: 'rgba(0, 0, 255, 0.1)' }} onClick={() => showPopupHandler('quality')}></div>
      </div>

      <div className="review-input">
        <h2>📝 Submit Your Review:</h2>
        <textarea
          id="full-review"
          rows="4"
          cols="50"
          placeholder="Type your full review about the shoe here... 🛒"
        />
        <button onClick={submitReview}>Submit Review</button>
      </div>

      <div className={`popup-overlay ${showPopup ? 'active' : ''}`} onClick={() => setShowPopup('')}></div>

      {showPopup && (
        <div id={`${showPopup}-popup`} className="popup">
          {updatePopupContents(aspectSentiments[showPopup])}
          <button onClick={() => showPopupHandler('')}>Close</button>
        </div>
      )}
    </div>
  );
};

export default ProductDetail;
