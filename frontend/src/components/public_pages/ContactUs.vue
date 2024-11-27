<template>
    <div class="contact-us">
        <!-- <h2>Contact Us</h2> -->
        <p>If you have any questions, feel free to reach out to us using the form below or through our contact details.
        </p>

        <h3>Email</h3>
        <p>support@platform.com</p>

        <h3>Phone</h3>
        <p>+971 (123) 456-7890</p>

        <h3>Our Office</h3>
        <p>VIRTUAL, NO WHERE</p>

        <h3>Get In Touch</h3>
        <form>
            <input type="text" placeholder="Your Name" required /><br />
            <input type="email" placeholder="Your Email" required /><br />
            <textarea placeholder="Your Message" required></textarea><br />
            <button type="submit">Send Message</button>
        </form>
    </div>
</template>

<script setup>
</script>

<style scoped>
.contact-us {
    padding: 0px;
}

h2 {
    color: #0056b3;
}
h3{
    color: #ff9900;
}
form {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

input,
textarea {
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
}

button {
    padding: 10px;
    background-color: #d0af37;
    color: white;
    border: none;
    border-radius: 5px;
}
</style>
