-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Apr 16, 2026 at 08:30 AM
-- Server version: 8.4.3
-- PHP Version: 8.3.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `libreria_virtual`
--

-- --------------------------------------------------------

--
-- Table structure for table `libros`
--

CREATE TABLE `libros` (
  `id` int NOT NULL,
  `titulo` varchar(150) NOT NULL,
  `autor` varchar(100) NOT NULL,
  `descripcion` text,
  `precio` decimal(10,2) NOT NULL,
  `categoria` varchar(50) DEFAULT NULL,
  `imagen_url` varchar(255) DEFAULT 'default_book.png',
  `stock` int DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `libros`
--

INSERT INTO `libros` (`id`, `titulo`, `autor`, `descripcion`, `precio`, `categoria`, `imagen_url`, `stock`) VALUES
(1, 'Clean Code', 'Robert C. Martin', 'Manual de código limpio.', 35.50, 'Programación', '/static/uploads/cleancode.jpg', 0),
(2, '1984', 'George Orwell', 'Novela distópica.', 9.50, 'Novela', '/static/uploads/1984.jpg', 0),
(3, 'Hábitos Atómicos', 'James Clear', 'Mejora tus rutinas.', 18.90, 'Bienestar', '/static/uploads/habitos.jpg', 0),
(4, 'El Programador Pragmático', 'Andrew Hunt', 'Mejores prácticas para desarrollar software.', 32.00, 'Programación', '/static/uploads/pragmatic.jpg', 0),
(5, 'Dune', 'Frank Herbert', 'Obra maestra de la ciencia ficción.', 12.50, 'Novela', '/static/uploads/dune.jpg', 0),
(6, 'El Poder del Ahora', 'Eckhart Tolle', 'Guía para el crecimiento personal y espiritual.', 15.90, 'Bienestar', '/static/uploads/ahora.jpg', 0),
(7, 'The Mythical Man-Month', 'Frederick P. Brooks Jr.', 'Ensayos sobre ingeniería de software y gestión de proyectos.', 31.20, 'Programación', '/static/uploads/mythical-man.jpg', 10),
(8, 'Cien años de soledad', 'Gabriel García Márquez', 'La cumbre del realismo mágico.', 14.25, 'Novela', '/static/uploads/soledad.jpg', 10),
(9, 'Piense y hágase rico', 'Napoleon Hill', 'Clásico del crecimiento y éxito personal.', 12.00, 'Bienestar', '/static/uploads/rico.jpg', 8),
(10, 'Sapiens', 'Yuval Noah Harari', 'Breve historia de la humanidad.', 21.90, 'Divulgación Científica', '/static/uploads/sapiens.jpg', 20),
(11, 'Refactoring', 'Martin Fowler', 'Mejorando el diseño del código existente.', 42.50, 'Programación', '/static/uploads/refactoring.jpg', 5),
(12, 'Cosmos', 'Carl Sagan', 'Un recorrido por el universo y la ciencia.', 19.95, 'Divulgación Científica', '/static/uploads/cosmos.jpg', 12),
(13, 'El resplandor', 'Stephen King', 'Un clásico moderno del terror psicológico.', 11.40, 'Novela', '/static/uploads/resplandor.jpg', 7),
(14, 'El hombre en busca de sentido', 'Viktor Frankl', 'Lecciones de resiliencia en condiciones extremas.', 13.50, 'Bienestar', '/static/uploads/sentido.jpg', 9),
(15, 'Don''t Make Me Think', 'Steve Krug', 'Un enfoque práctico a la usabilidad web.', 25.00, 'Diseño', '/static/uploads/dont-think.jpg', 12),
(16, 'Steve Jobs', 'Walter Isaacson', 'La biografía exclusiva del fundador de Apple.', 22.90, 'Biografía', '/static/uploads/jobs.jpg', 5),
(17, 'El Cisne Negro', 'Nassim Nicholas Taleb', 'El impacto de lo altamente improbable.', 24.00, 'Ensayo', '/static/uploads/cisne-negro.jpg', 8),
(18, 'Design of Everyday Things', 'Don Norman', 'Por qué algunos productos nos vuelven locos.', 19.50, 'Diseño', '/static/uploads/everyday-things.jpg', 10),
(19, 'Open', 'Andre Agassi', 'Una de las mejores memorias deportivas jamás escritas.', 16.95, 'Biografía', '/static/uploads/open.jpg', 14),
(20, 'La sociedad del cansancio', 'Byung-Chul Han', 'Análisis crítico sobre la autoexplotación moderna.', 12.00, 'Ensayo', '/static/uploads/cansancio.jpg', 20),
(21, 'The Design of Childhood', 'Alexandra Lange', 'Cómo los objetos influyen en el crecimiento.', 28.00, 'Diseño', '/static/uploads/childhood-design.jpg', 4),
(22, 'Elon Musk', 'Ashlee Vance', 'El empresario que anticipa el futuro.', 21.00, 'Biografía', '/static/uploads/musk.jpg', 7),
(23, 'Padre Rico, Padre Pobre', 'Robert Kiyosaki', 'Lecciones sobre libertad financiera y dinero.', 15.50, 'Finanzas', '/static/uploads/padre-rico.jpg', 25),
(24, 'La Psicología del Dinero', 'Morgan Housel', 'Cómo nuestras emociones afectan nuestras finanzas.', 18.00, 'Finanzas', '/static/uploads/psicologia-dinero.jpg', 15),
(25, 'El infinito en un junco', 'Irene Vallejo', 'La invención de los libros en el mundo antiguo.', 23.50, 'Historia', '/static/uploads/infinito-junco.jpg', 10),
(26, 'Kitchen Confidential', 'Anthony Bourdain', 'Aventuras en el mundo de la alta cocina.', 14.95, 'Cocina', '/static/uploads/kitchen-confidential.jpg', 8),
(27, 'Salt, Fat, Acid, Heat', 'Samin Nosrat', 'Los cuatro elementos que dominan el sabor.', 32.00, 'Cocina', '/static/uploads/salt-fat.jpg', 6),
(28, 'Guns, Germs, and Steel', 'Jared Diamond', 'Por qué algunas civilizaciones prosperan más que otras.', 19.00, 'Historia', '/static/uploads/guns-germs.jpg', 9),
(29, 'The Intelligent Investor', 'Benjamin Graham', 'La biblia del valor en la inversión.', 26.50, 'Finanzas', '/static/uploads/intelligent-investor.jpg', 11),
(30, 'Fahrenheit 451', 'Ray Bradbury', 'Una visión aterradora de un futuro sin libros.', 10.80, 'Novela', '/static/uploads/fahrenheit.jpg', 15),
(31, 'Design Patterns', 'Erich Gamma et al.', 'Patrones de diseño de software reutilizables.', 45.00, 'Programación', '/static/uploads/design-patterns.jpg', 6),
(32, 'Los 7 hábitos de la gente altamente efectiva', 'Stephen Covey', 'Principios fundamentales para la efectividad personal.', 22.00, 'Bienestar', '/static/uploads/7-habitos.jpg', 18),
(33, 'Breve historia del tiempo', 'Stephen Hawking', 'Desde el big bang a los agujeros negros.', 14.50, 'Divulgación Científica', '/static/uploads/breve-historia.jpg', 10),
(34, 'Meditaciones', 'Marco Aurelio', 'Pensamientos estoicos de un emperador romano.', 11.20, 'Bienestar', '/static/uploads/meditaciones.jpg', 25),
(35, 'Leonardo da Vinci', 'Walter Isaacson', 'La biografía definitiva del mayor genio de la historia.', 24.90, 'Biografía', '/static/uploads/davinci.jpg', 7),
(36, 'El hombre más rico de Babilonia', 'George S. Clason', 'Secretos para el éxito y la prosperidad financiera.', 13.00, 'Finanzas', '/static/uploads/babilonia.jpg', 30),
(37, 'Crónica de una muerte anunciada', 'Gabriel García Márquez', 'Un relato fascinante sobre el honor y el destino.', 9.90, 'Novela', '/static/uploads/cronica.jpg', 12),
(38, 'Robar como un artista', 'Austin Kleon', 'Diez cosas que nadie te dijo sobre ser creativo.', 15.00, 'Diseño', '/static/uploads/robar-artista.jpg', 20),
(39, 'El gen egoísta', 'Richard Dawkins', 'La perspectiva de la evolución desde el gen.', 18.50, 'Divulgación Científica', '/static/uploads/gen-egoista.jpg', 8),
(40, 'SPQR: Una historia de la antigua Roma', 'Mary Beard', 'Un recorrido magistral por la historia de Roma.', 22.00, 'Historia', '/static/uploads/spqr.jpg', 11),
(41, 'Flour Water Salt Yeast', 'Ken Forkish', 'La biblia del pan artesanal hecho en casa.', 29.90, 'Cocina', '/static/uploads/bread-bible.jpg', 5),
(42, 'The Clean Coder', 'Robert C. Martin', 'Código de conducta para programadores profesionales.', 33.00, 'Programación', '/static/uploads/clean-coder.jpg', 14);
-- --------------------------------------------------------

--
-- Table structure for table `pedidos`
--

CREATE TABLE `pedidos` (
  `id` int NOT NULL,
  `usuario_id` int DEFAULT NULL,
  `fecha` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `total` decimal(10,2) NOT NULL,
  `estado` enum('pendiente','enviado','entregado') DEFAULT 'pendiente'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `es_admin` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `email`, `password`, `direccion`, `es_admin`) VALUES
(2, '', 'aa@aa', '961b6dd3ede3cb8ecbaacbd68de040cd78eb2ed5889130cceb4c49268ea4d506', NULL, 0),
(4, '', 'aa@aaa', '961b6dd3ede3cb8ecbaacbd68de040cd78eb2ed5889130cceb4c49268ea4d506', NULL, 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `libros`
--
ALTER TABLE `libros`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `pedidos`
--
ALTER TABLE `pedidos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indexes for table `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `libros`
--
ALTER TABLE `libros`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `pedidos`
--
ALTER TABLE `pedidos`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `pedidos`
--
ALTER TABLE `pedidos`
  ADD CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
