-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Время создания: Дек 19 2024 г., 19:21
-- Версия сервера: 10.4.32-MariaDB
-- Версия PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `test1`
--

-- --------------------------------------------------------

--
-- Структура таблицы `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `data` text NOT NULL,
  `status` text DEFAULT NULL,
  `date_time` datetime DEFAULT NULL,
  `url` text NOT NULL,
  `id_telegram` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `user`
--

INSERT INTO `user` (`id`, `user_id`, `data`, `status`, `date_time`, `url`, `id_telegram`) VALUES
(21, 536551, 'body:nth-child(2) > div:nth-child(1) > main.bg-white:nth-child(3) > div.container.flex.flex-col.gap-8.px-4.py-16:nth-child(1)', '1', '2024-12-17 20:51:55', 'https://q-parser.ru/', 0),
(22, 947480, 'body:nth-child(2) > div:nth-child(1) > main.bg-white:nth-child(3) > div.container.flex.flex-col.gap-8.px-4.py-16:nth-child(1)', '1', '2024-12-17 20:54:41', 'https://q-parser.ru/', 0),
(23, 788411, 'body:nth-child(2) > div:nth-child(1) > main.bg-white:nth-child(3) > div.container.flex.flex-col.gap-8.px-4.py-16:nth-child(1)', '1', '2024-12-18 18:05:03', 'https://q-parser.ru/', 0),
(26, 123456, 'body > div.pagecontainer > div > div:nth-child(27) > div > div.sd62b6GxXGP8Gj9thOmes > div', '1', '2024-12-19 12:07:36', 'https://www.aviasales.kz/map?center=27.606,2.842&params=ALAANYWHERE1&zoom=4.44', 2020036419),
(27, 501798, 'body:nth-child(2) > div:nth-child(1) > main.bg-white:nth-child(3) > div.container.flex.flex-col.gap-8.px-4.py-16:nth-child(1)', '1', '2024-12-19 11:37:35', 'https://q-parser.ru/', 0);

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
