<template>
    <div class="clients-and-stars">
        <!-- Marquee Customers Section -->
        <div class="marquee">
            <h2>Top Patrons</h2>
            <div class="brands-wrapper">
                <div v-for="(brand, index) in brands" :key="index" class="brand">
                    <img :src="`src/assets/images/${brand.image}`" alt="Brand Logo" />
                    
                </div>
            </div>
        </div>

        <!-- Stars Section -->
        <div class="stars">
            <h2>Treding Stars</h2>
            <div class="stars-wrapper">
                <div v-for="(influencer, index) in influencers" :key="index" class="influencer">
                    <img :src="`src/assets/images/${influencer.image}`" alt="Influencer" />
                    <!-- <p>{{ influencer.name }}</p> -->
                </div>
            </div>
        </div>
    </div>
</template>


<script setup>
import { ref } from 'vue';

const brands = [
    { image: 'brand1.png' },
    { image: 'brand2.png' },
    { image: 'brand3.png' },
    { image: 'brand4.png' },
    { image: 'brand5.png' },
    { image: 'brand6.png' },
    { image: 'brand7.png' },
    { image: 'brand8.png' },
    // { image: 'brand9.png' },
    // { image: 'brand10.png' },
    // { image: 'brand11.png' },
    // { image: 'brand12.png' },
    // { image: 'brand13.png' },
    // { image: 'brand14.png' },
    // { image: 'brand15.png' },
];

const influencers = [
    { name: 'Influencer 1', image: 'in1.png' },
    { name: 'Influencer 2', image: 'in2.png' },
    { name: 'Influencer 3', image: 'in3.png' },
    { name: 'Influencer 4', image: 'in4.png' },
    { name: 'Influencer 5', image: 'in5.png' },
    { name: 'Influencer 6', image: 'in6.png' },
    { name: 'Influencer 7', image: 'in7.png' },
    { name: 'Influencer 8', image: 'in8.png' },
    // { name: 'Influencer 9', image: 'influencer9.png' },
    // { name: 'Influencer 10', image: 'influencer10.png' },
    // { name: 'Influencer 11', image: 'influencer11.png' },
    // { name: 'Influencer 12', image: 'influencer12.png' },
];
</script>
<!-- 
<style scoped>
.clients-and-stars {
    padding: 0px;
}

/* Marquee Customers Section */
.marquee {
    margin-bottom: 20px;
    text-align: center;
}

.marquee h2 {
    font-size: 24px;
    font-weight: bold;
}

.brands-wrapper {
    overflow: hidden;
    width: 100%;
    /* Ensure brands don't overflow horizontally */
}

.brands-container {
    display: flex;
    gap: 20px;
    animation: marquee 20s linear infinite;
}

.brands {
    display: flex;
    gap: 20px;
}

.brand {
    width: 120px;
    height: 120px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.brand img {
    max-width: 100%;
    max-height: 100%;
}

/* Animation to move brands horizontally */
@keyframes marquee {
    0% {
        transform: translateX(100%);
    }

    100% {
        transform: translateX(-100%);
    }
}

/* Stars Section */
.stars {
    margin-top: 50px;
    text-align: center;
}

.stars h2 {
    font-size: 24px;
    font-weight: bold;
}

.stars-wrapper {
    overflow: hidden;
    width: 100%;
    /* Ensure influencers don't overflow horizontally */
}

.stars-container {
    display: flex;
    gap: 20px;
    animation: marquee-influencers 25s linear infinite;
}

.influencers {
    display: flex;
    gap: 20px;
}

.influencer {
    width: 120px;
    text-align: center;
}

.influencer img {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    object-fit: cover;
}

.influencer p {
    margin-top: 10px;
    font-size: 14px;
}

/* Animation to move influencers horizontally */
@keyframes marquee-influencers {
    0% {
        transform: translateX(100%);
    }

    100% {
        transform: translateX(-100%);
    }
}

/* Make sure the layout is responsive */
@media (max-width: 768px) {
    .brands-container {
        gap: 10px;
    }

    .stars-container {
        gap: 10px;
    }
}
</style> -->

<style scoped>
.clients-and-stars {
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 40px;
}

/* Section Titles */
.marquee h2,
.stars h2 {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
    text-align: center;
}

/* Grid Layout for Brands and Stars */
.brands-wrapper,
.stars-wrapper {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    /* Fixed 3 columns */
    gap: 20px;
    /* Spacing between items */
    justify-items: center;
    /* Center align items in their column */
    align-items: center;
    /* Vertically align items */
    width: 100%;
}

.brand,
.influencer {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    transition: transform 0.3s ease;
}

/* Brand Images */
.brand img,
.influencer img {
    width: 80px;
    height: 80px;
    object-fit: contain;
    border-radius: 50%;
    /* For influencers only */
    transition: transform 0.3s ease;
}

/* Hover Animation */
.brand:hover img,
.influencer:hover img {
    transform: scale(1.2);
    /* Zoom-in effect on hover */
}

/* Floating Animation for Subtle Movement */
@keyframes float {

    0%,
    100% {
        transform: translateY(0);
    }

    50% {
        transform: translateY(-5px);
    }
}

.brand img,
.influencer img {
    animation: float 3s ease-in-out infinite;
}

/* Text Under Influencer Images */
.influencer p {
    font-size: 14px;
    margin-top: 10px;
    text-align: center;
}

/* Responsive Adjustments */
@media (max-width: 768px) {

    .brands-wrapper,
    .stars-wrapper {
        grid-template-columns: repeat(2, 1fr);
        /* Reduce to 2 columns on smaller screens */
        gap: 15px;
    }
}

@media (max-width: 480px) {

    .brands-wrapper,
    .stars-wrapper {
        grid-template-columns: repeat(1, 1fr);
        /* Stack items in 1 column on very small screens */
    }
}
</style>
